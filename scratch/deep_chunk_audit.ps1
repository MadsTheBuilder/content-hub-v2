$dir = "c:\Users\madhu\Claude cowork\Content Hub\graphify-out"
Write-Host "=== SOURCE FILE COVERAGE PER CHUNK ==="
for ($i = 1; $i -le 10; $i++) {
    $path = Join-Path $dir (".graphify_chunk_{0:D2}.json" -f $i)
    $json = Get-Content $path -Raw | ConvertFrom-Json
    $sources = @()
    foreach ($node in $json.nodes) {
        if ($node.source_file) {
            $sources += $node.source_file
        }
    }
    $unique = $sources | Sort-Object -Unique
    $mktg = ($unique | Where-Object { $_ -match "tmp_marketingskills" }).Count
    $vault = ($unique | Where-Object { $_ -match "Content-Hub-Vault" }).Count
    $frontend = ($unique | Where-Object { $_ -match "^frontend/" }).Count
    $supabase = ($unique | Where-Object { $_ -match "^supabase/" }).Count
    $other = $unique.Count - $mktg - $vault - $frontend - $supabase
    Write-Host ""
    Write-Host "--- Chunk $i ---"
    Write-Host "  Total unique source files: $($unique.Count)"
    Write-Host "  tmp_marketingskills: $mktg"
    Write-Host "  Content-Hub-Vault: $vault"
    Write-Host "  frontend/: $frontend"  
    Write-Host "  supabase/: $supabase"
    Write-Host "  other: $other"
    if ($mktg -gt 0) {
        Write-Host "  [MARKETINGSKILLS FILES]:"
        foreach ($f in ($unique | Where-Object { $_ -match "tmp_marketingskills" })) {
            Write-Host "    $f"
        }
    }
}
