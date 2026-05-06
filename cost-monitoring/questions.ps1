# questions.ps1

$API_URL = "http://127.0.0.1:8000/ask"

$QUESTIONS = @(
  "Explain Kubernetes in one line",
  "What is a Kubernetes Pod?",
  "Explain ConfigMaps vs Secrets"
)

foreach ($q in $QUESTIONS) {
  Write-Host "Asking: $q"

  Invoke-WebRequest `
    -Uri $API_URL `
    -Method GET `
    -Body @{ q = $q }

  Start-Sleep -Seconds 1
}