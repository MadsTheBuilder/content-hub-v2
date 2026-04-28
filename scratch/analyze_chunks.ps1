$dir = "c:\Users\madhu\Claude cowork\Content Hub\graphify-out"
Get-ChildItem "$dir\.graphify_chunk_*.json" | ForEach-Object {
    $name = $_.Name
    $sz = $_.Length
    $c = Get-Content $_.FullName -Raw
    try {
        $j = $c | ConvertFrom-Json
        $n = 0; $e = 0
        if ($j.nodes) { $n = $j.nodes.Count }
        if ($j.edges) { $e = $j.edges.Count }
        Write-Host "$name | sz=$sz | nodes=$n | edges=$e | in_tok=$($j.input_tokens) | out_tok=$($j.output_tokens)"
    } catch {
        Write-Host "$name | sz=$sz | INVALID_JSON"
    }
}
