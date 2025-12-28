# Script to match Rimworld armor to FF/SA armor and merge helmets/prestige

$ErrorActionPreference = "Stop"

# Function to parse protection track from markdown
function Parse-ProtectionTrack {
    param($content)
    
    $track = @{}
    # Find the protection row specifically - must have "Protection" in the first column
    $lines = $content -split "`n"
    foreach ($line in $lines) {
        # More specific regex: must start with | and "Protection", then only digits
        # Use word boundaries and explicit digit matching
        if ($line -match '^\|\s*Protection\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)') {
            try {
                # Extract and validate each value
                $values = @($Matches[1], $Matches[2], $Matches[3], $Matches[4], $Matches[5], $Matches[6], $Matches[7])
                $allNumeric = $true
                foreach ($val in $values) {
                    if ($val -notmatch '^\d+$') {
                        $allNumeric = $false
                        break
                    }
                }
                
                if ($allNumeric) {
                    $track[1] = [int]$values[0]
                    $track[2] = [int]$values[1]
                    $track[3] = [int]$values[2]
                    $track[4] = [int]$values[3]
                    $track[5] = [int]$values[4]
                    $track[6] = [int]$values[5]
                    $track[7] = [int]$values[6]
                    return $track
                }
            } catch {
                # Skip if conversion fails
                continue
            }
        }
    }
    return $null
}

# Function to compare protection tracks
function Compare-ProtectionTracks {
    param($track1, $track2)
    
    if ($null -eq $track1 -or $null -eq $track2) { return 0 }
    
    $score = 0
    for ($i = 1; $i -le 7; $i++) {
        if ($track1.ContainsKey($i) -and $track2.ContainsKey($i)) {
            $diff = [Math]::Abs($track1[$i] - $track2[$i])
            $score += (7 - $diff)
        }
    }
    return $score
}

# Function to get tech level from content
function Get-TechLevel {
    param($content)
    
    if ($content -match 'Tech Level[:\s]*(\w+)') {
        return $Matches[1]
    }
    if ($content -match '\*\*Tech Level:\*\*\s*(\w+)') {
        return $Matches[1]
    }
    return $null
}

# Function to check name similarity
function Get-NameSimilarity {
    param($name1, $name2)
    
    $name1 = $name1.ToLower() -replace '[^a-z0-9]', ''
    $name2 = $name2.ToLower() -replace '[^a-z0-9]', ''
    
    if ($name1 -eq $name2) { return 100 }
    if ($name1 -like "*$name2*" -or $name2 -like "*$name1*") { return 80 }
    
    $keywords1 = @($name1 -split '-|_| ')
    $keywords2 = @($name2 -split '-|_| ')
    $common = ($keywords1 | Where-Object { $keywords2 -contains $_ }).Count
    if ($common -gt 0) { return 60 + ($common * 10) }
    
    return 0
}

# Load Rimworld armor (excluding helmets and prestige - will merge later)
Write-Output "Loading Rimworld armor..."
$rimworldArmor = @()
$rimworldHelmets = @{}  # Must be hashtable for ContainsKey
$rimworldPrestige = @{}  # Must be hashtable for ContainsKey

Get-ChildItem "RULES\Combat\Armor\Rimworld" -Recurse -Filter "*.md" | ForEach-Object {
    try {
        $fileName = $_.FullName
        $content = Get-Content $fileName -Raw
        $protectionTrack = Parse-ProtectionTrack $content
        if ($null -eq $protectionTrack -or $protectionTrack.Count -ne 7) {
            Write-Warning "Skipping $($_.Name) - invalid protection track"
            continue
        }
        # Validate all values are integers
        $allValid = $true
        for ($i = 1; $i -le 7; $i++) {
            if (-not $protectionTrack.ContainsKey($i) -or -not ($protectionTrack[$i] -is [int])) {
                Write-Warning "Skipping $($_.Name) - invalid track value at index $i : $($protectionTrack[$i])"
                $allValid = $false
                break
            }
        }
        if (-not $allValid) { continue }
        
        $name = $_.BaseName
        $techLevel = Get-TechLevel $content
        
        if ($name -like "*Helmet*" -or $name -like "*Hat*" -or $name -like "*Cap*") {
            # Extract base name (remove -Helmet, etc.)
            $baseName = $name -replace '-(Helmet|Hat|Cap).*$', ''
            if ([string]::IsNullOrEmpty($baseName)) {
                Write-Warning "Skipping $name - empty base name after extraction"
                continue
            }
            
            # Validate protection track first - must be hashtable (already validated above, but double-check)
            if ($null -eq $protectionTrack -or $protectionTrack -isnot [hashtable]) {
                Write-Warning "Skipping helmet $name - invalid protection track type: $($protectionTrack.GetType().FullName)"
                continue
            }
            
            try {
                # Create new array if needed
                if (-not $rimworldHelmets.ContainsKey($baseName)) {
                    $rimworldHelmets[$baseName] = @()
                }
                
                # Create helmet object
                $helmetObj = [PSCustomObject]@{
                    Name = $name
                    File = $_.FullName
                    ProtectionTrack = $protectionTrack
                    TechLevel = $techLevel
                    Content = $content
                }
                
                # Add to array using +=
                $rimworldHelmets[$baseName] += $helmetObj
            } catch {
                Write-Warning "Error adding helmet $name (base: $baseName): $_"
                Write-Warning "ProtectionTrack type in error: $($protectionTrack.GetType().FullName)"
                continue
            }
        } elseif ($name -like "*Prestige*") {
            $baseName = $name -replace '-Prestige.*$', ''
            if ([string]::IsNullOrEmpty($baseName)) {
                Write-Warning "Skipping $name - empty base name after extraction"
                continue
            }
            try {
                if ($null -eq $rimworldPrestige[$baseName]) {
                    $rimworldPrestige[$baseName] = @()
                }
                $prestigeList = $rimworldPrestige[$baseName]
                $prestigeList += [PSCustomObject]@{
                    Name = $name
                    File = $_.FullName
                    ProtectionTrack = $protectionTrack
                    TechLevel = $techLevel
                    Content = $content
                }
                $rimworldPrestige[$baseName] = $prestigeList
            } catch {
                Write-Warning "Error adding prestige $name (base: $baseName): $_"
                continue
            }
        } else {
            $rimworldArmor += [PSCustomObject]@{
                Name = $name
                File = $_.FullName
                ProtectionTrack = $protectionTrack
                TechLevel = $techLevel
                Content = $content
            }
        }
    } catch {
        Write-Warning "Error processing $($_.Name): $_"
        Write-Warning "Stack: $($_.ScriptStackTrace)"
        continue
    }
}

Write-Output "Found $($rimworldArmor.Count) Rimworld armor items"
Write-Output "Found $($rimworldHelmets.Keys.Count) armor sets with helmets"
Write-Output "Found $($rimworldPrestige.Keys.Count) armor sets with prestige versions"

# Merge helmets and prestige into base armor
foreach ($armor in $rimworldArmor) {
    $baseName = $armor.Name -replace '-.*$', ''
    
    # Validate armor protection track first
    if ($null -eq $armor.ProtectionTrack -or $armor.ProtectionTrack.Count -ne 7) {
        Write-Warning "Skipping merge for $($armor.Name) - invalid protection track"
        continue
    }
    
    # Validate all armor protection values are integers
    $armorTrackValid = $true
    for ($i = 1; $i -le 7; $i++) {
        if (-not $armor.ProtectionTrack.ContainsKey($i) -or -not ($armor.ProtectionTrack[$i] -is [int])) {
            Write-Warning "Skipping merge for $($armor.Name) - invalid track value at index $i"
            $armorTrackValid = $false
            break
        }
    }
    if (-not $armorTrackValid) { continue }
    
    # Merge helmet if exists
    if ($null -ne $rimworldHelmets[$baseName] -and $rimworldHelmets[$baseName].Count -gt 0) {
        $helmet = $rimworldHelmets[$baseName] | Select-Object -First 1
        if ($null -eq $helmet.ProtectionTrack -or $helmet.ProtectionTrack.Count -ne 7) {
            Write-Warning "Skipping helmet merge for $($armor.Name) - invalid helmet protection track"
        } else {
            # Validate all helmet protection values are integers
            $helmetTrackValid = $true
            for ($i = 1; $i -le 7; $i++) {
                if (-not $helmet.ProtectionTrack.ContainsKey($i) -or -not ($helmet.ProtectionTrack[$i] -is [int])) {
                    $helmetTrackValid = $false
                    break
                }
            }
            
            if ($helmetTrackValid) {
                # Average protection tracks
                for ($i = 1; $i -le 7; $i++) {
                    $armor.ProtectionTrack[$i] = [Math]::Round(($armor.ProtectionTrack[$i] + $helmet.ProtectionTrack[$i]) / 2)
                }
                # Add properties if they don't exist
                if (-not ($armor.PSObject.Properties.Name -contains 'HasHelmet')) {
                    $armor | Add-Member -MemberType NoteProperty -Name 'HasHelmet' -Value $true
                } else {
                    $armor.HasHelmet = $true
                }
                if (-not ($armor.PSObject.Properties.Name -contains 'HelmetContent')) {
                    $armor | Add-Member -MemberType NoteProperty -Name 'HelmetContent' -Value $helmet.Content
                } else {
                    $armor.HelmetContent = $helmet.Content
                }
            } else {
                Write-Warning "Skipping helmet merge for $($armor.Name) - helmet has non-integer protection values"
            }
        }
    }
    
    # Merge prestige if exists
    if ($null -ne $rimworldPrestige[$baseName] -and $rimworldPrestige[$baseName].Count -gt 0) {
        $prestige = $rimworldPrestige[$baseName] | Select-Object -First 1
        if ($prestige.ProtectionTrack -and $armor.ProtectionTrack -and $prestige.ProtectionTrack.Count -eq 7 -and $armor.ProtectionTrack.Count -eq 7) {
            # Use higher values - validate all values are integers first
            $canMerge = $true
            for ($i = 1; $i -le 7; $i++) {
                if (-not ($armor.ProtectionTrack[$i] -is [int]) -or -not ($prestige.ProtectionTrack[$i] -is [int])) {
                    $canMerge = $false
                    break
                }
            }
            if ($canMerge) {
                for ($i = 1; $i -le 7; $i++) {
                    if ($prestige.ProtectionTrack[$i] -gt $armor.ProtectionTrack[$i]) {
                        $armor.ProtectionTrack[$i] = $prestige.ProtectionTrack[$i]
                    }
                }
                $armor.HasPrestige = $true
                $armor.PrestigeContent = $prestige.Content
            }
        }
    }
}

# Load FF armor
Write-Output "Loading Fighting Fantasy armor..."
$ffArmor = @()
Get-ChildItem "RULES\Combat\Armor\Fighting-Fantasy" -Filter "*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $protectionTrack = Parse-ProtectionTrack $content
    if ($protectionTrack) {
        $ffArmor += [PSCustomObject]@{
            Name = $_.BaseName
            File = $_.FullName
            ProtectionTrack = $protectionTrack
            Content = $content
        }
    }
}

Write-Output "Found $($ffArmor.Count) FF armor items"

# Load SA armor
Write-Output "Loading Stellar Adventures armor..."
$saArmor = @()
Get-ChildItem "RULES\Combat\Armor\Stellar-Adventures" -Filter "*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $protectionTrack = Parse-ProtectionTrack $content
    if ($protectionTrack) {
        $saArmor += [PSCustomObject]@{
            Name = $_.BaseName
            File = $_.FullName
            ProtectionTrack = $protectionTrack
            Content = $content
        }
    }
}

Write-Output "Found $($saArmor.Count) SA armor items"

# Match Rimworld to FF/SA
$matches = @()
$usedFF = @{}
$usedSA = @{}

foreach ($rw in $rimworldArmor) {
    $bestMatch = $null
    $bestScore = 0
    $matchType = $null
    
    $shouldMatchFF = $rw.TechLevel -in @("Neolithic", "Medieval", "Industrial")
    $shouldMatchSA = $rw.TechLevel -in @("Spacer", "Ultra") -or $rw.Name -like "*Space*" -or $rw.Name -like "*Marine*" -or $rw.Name -like "*Power*"
    
    $targetList = @()
    if ($shouldMatchFF -and -not $shouldMatchSA) {
        $targetList = $ffArmor | ForEach-Object { [PSCustomObject]@{Armor=$_; Type="FF"} }
    } elseif ($shouldMatchSA) {
        $targetList = $saArmor | ForEach-Object { [PSCustomObject]@{Armor=$_; Type="SA"} }
    } else {
        $targetList = ($ffArmor | ForEach-Object { [PSCustomObject]@{Armor=$_; Type="FF"}}) + ($saArmor | ForEach-Object { [PSCustomObject]@{Armor=$_; Type="SA"}})
    }
    
    foreach ($target in $targetList) {
        $t = $target.Armor
        $isUsed = if ($target.Type -eq "FF") { $usedFF.ContainsKey($t.Name) } else { $usedSA.ContainsKey($t.Name) }
        if ($isUsed) { continue }
        
        $nameScore = Get-NameSimilarity $rw.Name $t.Name
        $protectionScore = Compare-ProtectionTracks $rw.ProtectionTrack $t.ProtectionTrack
        
        $score = 0
        if ($nameScore -gt 70) {
            $score = 100 + $protectionScore
        } else {
            $score = ($nameScore * 0.3) + ($protectionScore * 0.7)
        }
        
        if ($score -gt $bestScore) {
            $bestScore = $score
            $bestMatch = $t
            $matchType = $target.Type
        }
    }
    
    if ($bestMatch -and $bestScore -gt 20) {
        $matches += [PSCustomObject]@{
            Rimworld = $rw.Name
            Target = $bestMatch.Name
            Type = $matchType
            Score = [Math]::Round($bestScore, 2)
            RimworldFile = $rw.File
            TargetFile = $bestMatch.File
            HasHelmet = if ($rw.HasHelmet) { $true } else { $false }
            HasPrestige = if ($rw.HasPrestige) { $true } else { $false }
        }
        
        if ($matchType -eq "FF") {
            $usedFF[$bestMatch.Name] = $true
        } else {
            $usedSA[$bestMatch.Name] = $true
        }
    }
}

Write-Output "`nFound $($matches.Count) armor matches:"
$matches | Format-Table -AutoSize

# Save matches
$matches | ConvertTo-Json -Depth 10 | Out-File "rimworld_to_aff_armor_matches.json" -Encoding UTF8
Write-Output "`nMatches saved to rimworld_to_aff_armor_matches.json"

