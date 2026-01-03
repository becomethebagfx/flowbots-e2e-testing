# C:\flowbots_lab\scripts\monitor_resources.ps1
# Resource monitoring script for FLOWBOTS E2E testing

function Get-ResourceStatus {
    $cpu = (Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples.CookedValue
    $mem = (Get-Counter '\Memory\% Committed Bytes In Use').CounterSamples.CookedValue
    $disk = (Get-PSDrive C).Free / 1GB

    return @{
        cpu_percent = [math]::Round($cpu, 1)
        memory_percent = [math]::Round($mem, 1)
        disk_free_gb = [math]::Round($disk, 1)
        timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    }
}

function Test-ResourcesOK {
    $status = Get-ResourceStatus
    $ok = ($status.cpu_percent -lt 85) -and
          ($status.memory_percent -lt 90) -and
          ($status.disk_free_gb -gt 10)

    $result = @{
        ok = $ok
        status = $status
    }

    return $result | ConvertTo-Json
}

# If called directly, run the check
if ($MyInvocation.InvocationName -ne '.') {
    Test-ResourcesOK
}
