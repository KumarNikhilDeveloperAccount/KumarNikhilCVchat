param(
    [Parameter(Mandatory = $true)]
    [string]$PdfPath
)

function Decode-Ascii85 {
    param([string]$Data)

    $bytes = New-Object System.Collections.Generic.List[byte]
    $group = New-Object System.Collections.Generic.List[int]
    $chars = ($Data -replace '\s', '').ToCharArray()
    $index = 0

    while ($index -lt $chars.Length) {
        $char = $chars[$index]
        $index += 1
        if ($char -eq '~') { break }
        if ($char -eq 'z') {
            if ($group.Count -ne 0) { throw "Invalid ASCII85 stream." }
            $bytes.AddRange([byte[]](0, 0, 0, 0))
            continue
        }

        $value = [int][char]$char
        if ($value -lt 33 -or $value -gt 117) { continue }
        $group.Add($value - 33)

        if ($group.Count -eq 5) {
            [uint32]$tuple = 0
            foreach ($digit in $group) {
                $tuple = $tuple * 85 + [uint32]$digit
            }
            $bytes.Add([byte](($tuple -shr 24) -band 0xFF))
            $bytes.Add([byte](($tuple -shr 16) -band 0xFF))
            $bytes.Add([byte](($tuple -shr 8) -band 0xFF))
            $bytes.Add([byte]($tuple -band 0xFF))
            $group.Clear()
        }
    }

    if ($group.Count -gt 0) {
        $padding = 5 - $group.Count
        for ($i = 0; $i -lt $padding; $i++) {
            $group.Add(84)
        }
        [uint32]$tuple = 0
        foreach ($digit in $group) {
            $tuple = $tuple * 85 + [uint32]$digit
        }
        $temp = [byte[]](
            [byte](($tuple -shr 24) -band 0xFF),
            [byte](($tuple -shr 16) -band 0xFF),
            [byte](($tuple -shr 8) -band 0xFF),
            [byte]($tuple -band 0xFF)
        )
        for ($i = 0; $i -lt 4 - $padding; $i++) {
            $bytes.Add($temp[$i])
        }
    }

    return $bytes.ToArray()
}

function Inflate-Bytes {
    param([byte[]]$Bytes)

    $input = New-Object System.IO.MemoryStream
    $input.Write($Bytes, 0, $Bytes.Length)
    $input.Position = 0

    $output = New-Object System.IO.MemoryStream
    $input.ReadByte() | Out-Null
    $input.ReadByte() | Out-Null
    $deflate = New-Object System.IO.Compression.DeflateStream($input, [System.IO.Compression.CompressionMode]::Decompress)
    $deflate.CopyTo($output)
    $deflate.Dispose()
    $input.Dispose()
    $result = $output.ToArray()
    $output.Dispose()
    return $result
}

$raw = Get-Content -Raw -Path $PdfPath
$streams = [regex]::Matches($raw, 'stream\s*(.*?)\s*endstream', [System.Text.RegularExpressions.RegexOptions]::Singleline)
$decodedParts = New-Object System.Collections.Generic.List[string]

foreach ($stream in $streams) {
    $encoded = $stream.Groups[1].Value
    try {
        $asciiBytes = Decode-Ascii85 -Data $encoded
        $inflated = Inflate-Bytes -Bytes $asciiBytes
        $decodedParts.Add([System.Text.Encoding]::Latin1.GetString($inflated))
    } catch {
    }
}

$content = $decodedParts -join "`n"
$matches = [regex]::Matches($content, '\((?<text>(?:\\.|[^\\)])*)\)\s*Tj')
$arrayMatches = [regex]::Matches($content, '\[(?<items>.*?)\]\s*TJ', [System.Text.RegularExpressions.RegexOptions]::Singleline)
$lines = New-Object System.Collections.Generic.List[string]

foreach ($match in $matches) {
    $text = $match.Groups['text'].Value
    $text = $text -replace '\\\(', '('
    $text = $text -replace '\\\)', ')'
    $text = $text -replace '\\n', ' '
    $text = $text -replace '\\r', ' '
    $text = $text -replace '\\t', ' '
    $lines.Add($text)
}

foreach ($arrayMatch in $arrayMatches) {
    $itemMatches = [regex]::Matches($arrayMatch.Groups['items'].Value, '\((?<text>(?:\\.|[^\\)])*)\)')
    foreach ($itemMatch in $itemMatches) {
        $text = $itemMatch.Groups['text'].Value
        $text = $text -replace '\\\(', '('
        $text = $text -replace '\\\)', ')'
        $text = $text -replace '\\n', ' '
        $text = $text -replace '\\r', ' '
        $text = $text -replace '\\t', ' '
        $lines.Add($text)
    }
}

$clean = ($lines | Where-Object { $_.Trim() } | ForEach-Object { $_.Trim() }) -join "`n"
if (-not $clean) {
    $clean = $content
}
$clean
