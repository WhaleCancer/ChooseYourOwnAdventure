# Script to apply Rimworld matches to FF/SA weapon files
# Also handles armor matching and merging

$ErrorActionPreference = "Stop"

# Load matches
$matches = Get-Content "rimworld_to_aff_matches.json" | ConvertFrom-Json

Write-Output "Found $($matches.Count) weapon matches"

# Function to extract Rimworld stats from content
function Extract-RimworldStats {
    param($content)
    
    $stats = @{}
    
    # Extract damage track
    if ($content -match '\|\s*Damage\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)') {
        $stats.DamageTrack = @{
            1 = [int]$Matches[1]
            2 = [int]$Matches[2]
            3 = [int]$Matches[3]
            4 = [int]$Matches[4]
            5 = [int]$Matches[5]
            6 = [int]$Matches[6]
            7 = [int]$Matches[7]
        }
    }
    
    # Extract original Rimworld stats
    if ($content -match '\*\*Original Rimworld Damage:\*\*\s*([\d.~]+)') {
        $stats.OriginalDamage = $Matches[1]
    }
    if ($content -match '\*\*Original Rimworld DPS:\*\*\s*([\d.~]+)') {
        $stats.OriginalDPS = $Matches[1]
    }
    if ($content -match '\*\*Range:\*\*\s*([\d.]+)') {
        $stats.Range = $Matches[1]
    }
    if ($content -match '\*\*Tech Level:\*\*\s*(\w+)') {
        $stats.TechLevel = $Matches[1]
    }
    if ($content -match '\*\*Type:\*\*\s*(\w+)') {
        $stats.Type = $Matches[1]
    }
    if ($content -match '\*\*DLC:\*\*\s*(\w+)') {
        $stats.DLC = $Matches[1]
    }
    
    # Extract description
    if ($content -match '## Description\s*\n\s*\n(.*?)(?=\n\n|\Z)') {
        $stats.Description = $Matches[1].Trim()
    }
    
    return $stats
}

# Apply weapon matches
foreach ($match in $matches) {
    $rimworldContent = Get-Content $match.RimworldFile -Raw
    $targetContent = Get-Content $match.TargetFile -Raw
    
    $rimworldStats = Extract-RimworldStats $rimworldContent
    
    # Update target file with Rimworld statistics
    # Add Rimworld variant section before description
    $variantSection = @"

## Rimworld Statistics

**Source:** Rimworld $(if ($rimworldStats.DLC) { "$($rimworldStats.DLC) DLC" } else { "Core Game" }) ($($rimworldStats.TechLevel) Tech)

**Note:** Statistics converted from Rimworld values to Advanced Fighting Fantasy damage track system.

### Damage Track

| Roll | 1 | 2 | 3 | 4 | 5 | 6 | 7+ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Damage | $($rimworldStats.DamageTrack[1]) | $($rimworldStats.DamageTrack[2]) | $($rimworldStats.DamageTrack[3]) | $($rimworldStats.DamageTrack[4]) | $($rimworldStats.DamageTrack[5]) | $($rimworldStats.DamageTrack[6]) | $($rimworldStats.DamageTrack[7]) |

### Statistics

- **Original Rimworld Damage:** $($rimworldStats.OriginalDamage)
- **Original Rimworld DPS:** $($rimworldStats.OriginalDPS)
$(if ($rimworldStats.Range) { "- **Range:** $($rimworldStats.Range)" })
- **Type:** $($rimworldStats.Type)
- **Tech Level:** $($rimworldStats.TechLevel)

### Description

$($rimworldStats.Description)

"@
    
    # Insert before Description section
    if ($targetContent -match '(## Description)') {
        $newContent = $targetContent -replace '(## Description)', "$variantSection`n`n`$1"
        Set-Content $match.TargetFile -Value $newContent -Encoding UTF8
        Write-Output "Updated: $($match.Target) with Rimworld stats from $($match.Rimworld)"
    }
}

Write-Output "`nCompleted weapon updates"



