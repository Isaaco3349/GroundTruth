Set-Location $PSScriptRoot\..
$env:PYTHONPATH = "src"
uvicorn groundtruth.api:app --reload --port 8787
