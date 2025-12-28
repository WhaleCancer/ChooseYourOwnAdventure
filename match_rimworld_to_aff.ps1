# Script to match Rimworld weapons and armor to FF/SA items

$ErrorActionPreference = "Stop"

# Function to parse damage track from markdown
function Parse-DamageTrack {
    param($content)
    
    $track = @{}
    # Look for damage track table
    if ($content -match '\|.*Damage.*\|') {
        $lines = $content -split "`n"
        foreach ($line in $lines) {
            if ($line -match '\|\s*Damage\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)') {
                $track[1] = [int]$Matches[1]
                $track[2] = [int]$Matches[2]
                $track[3] = [int]$Matches[3]
                $track[4] = [int]$Matches[4]
                $track[5] = [int]$Matches[5]
                $track[6] = [int]$Matches[6]
                $track[7] = [int]$Matches[7]
                return $track
            }
        }
    }
    return $null
}

# Function to calculate similarity score between damage tracks
function Compare-DamageTracks {
    param($track1, $track2)
    
    if ($null -eq $track1 -or $null -eq $track2) { return 0 }
    
    $score = 0
    for ($i = 1; $i -le 7; $i++) {
        if ($track1.ContainsKey($i) -and $track2.ContainsKey($i)) {
            $diff = [Math]::Abs($track1[$i] - $track2[$i])
            $score += (7 - $diff)  # Higher score for closer values
        }
    }
    return $score
}

# Function to extract tech level from content
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

# Function to extract weapon type (melee/ranged) from content
function Get-WeaponType {
    param($content)
    
    if ($content -match 'Type[:\s]*(\w+)') {
        return $Matches[1]
    }
    if ($content -match '\*\*Type:\*\*\s*(\w+)') {
        return $Matches[1]
    }
    # Infer from name/description
    if ($content -match 'Ranged|Rifle|Pistol|Gun|Bow|Crossbow') {
        return "Ranged"
    }
    if ($content -match 'Melee|Sword|Axe|Mace|Club|Knife|Dagger') {
        return "Melee"
    }
    return $null
}

# Load all Rimworld weapons
Write-Output "Loading Rimworld weapons..."
$rimworldWeapons = @()
Get-ChildItem "RULES\Combat\Weapons\Rimworld" -Recurse -Filter "*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $damageTrack = Parse-DamageTrack $content
    if ($damageTrack) {
        $name = $_.BaseName
        $techLevel = Get-TechLevel $content
        $weaponType = Get-WeaponType $content
        
        # Skip helmets - they'll be merged into armor
        if ($name -like "*Helmet*") { return }
        # Skip prestige - merge into normal
        if ($name -like "*Prestige*") { return }
        
        $rimworldWeapons += [PSCustomObject]@{
            Name = $name
            File = $_.FullName
            DamageTrack = $damageTrack
            TechLevel = $techLevel
            WeaponType = $weaponType
            Content = $content
        }
    }
}

Write-Output "Found $($rimworldWeapons.Count) Rimworld weapons"

# Load FF weapons
Write-Output "Loading Fighting Fantasy weapons..."
$ffWeapons = @()
Get-ChildItem "RULES\Combat\Weapons\Fighting-Fantasy" -Filter "*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $damageTrack = Parse-DamageTrack $content
    if ($damageTrack) {
        $ffWeapons += [PSCustomObject]@{
            Name = $_.BaseName
            File = $_.FullName
            DamageTrack = $damageTrack
            Content = $content
        }
    }
}

Write-Output "Found $($ffWeapons.Count) FF weapons"

# Load SA weapons
Write-Output "Loading Stellar Adventures weapons..."
$saWeapons = @()
Get-ChildItem "RULES\Combat\Weapons\Stellar-Adventures" -Filter "*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $damageTrack = Parse-DamageTrack $content
    if ($damageTrack) {
        $saWeapons += [PSCustomObject]@{
            Name = $_.BaseName
            File = $_.FullName
            DamageTrack = $damageTrack
            Content = $content
        }
    }
}

Write-Output "Found $($saWeapons.Count) SA weapons"

# Function to check name similarity
function Get-NameSimilarity {
    param($name1, $name2)
    
    $name1 = $name1.ToLower() -replace '[^a-z0-9]', ''
    $name2 = $name2.ToLower() -replace '[^a-z0-9]', ''
    
    # Direct match
    if ($name1 -eq $name2) { return 100 }
    
    # Contains match
    if ($name1 -like "*$name2*" -or $name2 -like "*$name1*") { return 80 }
    
    # Common keywords
    $keywords1 = @($name1 -split '-|_| ')
    $keywords2 = @($name2 -split '-|_| ')
    $common = ($keywords1 | Where-Object { $keywords2 -contains $_ }).Count
    if ($common -gt 0) { return 60 + ($common * 10) }
    
    return 0
}

# Match Rimworld to FF/SA
$matches = @()
$usedFF = @{}
$usedSA = @{}

# Sort by priority: exact name matches first, then by damage similarity
$sortedRimworld = $rimworldWeapons | Sort-Object { 
    $nameMatch = $false
    foreach ($ff in $ffWeapons) {
        if ((Get-NameSimilarity $_.Name $ff.Name) -gt 70) { $nameMatch = $true; break }
    }
    if (-not $nameMatch) {
        foreach ($sa in $saWeapons) {
            if ((Get-NameSimilarity $_.Name $sa.Name) -gt 70) { $nameMatch = $true; break }
        }
    }
    if ($nameMatch) { 0 } else { 1 }
}

foreach ($rw in $sortedRimworld) {
    $bestMatch = $null
    $bestScore = 0
    $matchType = $null
    
    # Determine if this should match FF (medieval/low tech) or SA (spacer/high tech)
    $shouldMatchFF = $rw.TechLevel -in @("Neolithic", "Medieval", "Industrial")
    $shouldMatchSA = $rw.TechLevel -in @("Spacer", "Ultra") -or $rw.Name -like "*Laser*" -or $rw.Name -like "*Plasma*" -or $rw.Name -like "*Charge*" -or $rw.Name -like "*Blaster*"
    
    $targetList = @()
    if ($shouldMatchFF -and -not $shouldMatchSA) {
        $targetList = $ffWeapons | ForEach-Object { [PSCustomObject]@{Weapon=$_; Type="FF"} }
    } elseif ($shouldMatchSA) {
        $targetList = $saWeapons | ForEach-Object { [PSCustomObject]@{Weapon=$_; Type="SA"} }
    } else {
        $targetList = ($ffWeapons | ForEach-Object { [PSCustomObject]@{Weapon=$_; Type="FF"}}) + ($saWeapons | ForEach-Object { [PSCustomObject]@{Weapon=$_; Type="SA"}})
    }
    
    foreach ($target in $targetList) {
        $t = $target.Weapon
        $isUsed = if ($target.Type -eq "FF") { $usedFF.ContainsKey($t.Name) } else { $usedSA.ContainsKey($t.Name) }
        if ($isUsed) { continue }
        
        # Check weapon type match (melee vs ranged)
        $targetType = Get-WeaponType $t.Content
        $typeMatch = $true
        if ($rw.WeaponType -and $targetType) {
            if ($rw.WeaponType -ne $targetType) {
                $typeMatch = $false
            }
        }
        
        # Calculate composite score
        $nameScore = Get-NameSimilarity $rw.Name $t.Name
        $damageScore = Compare-DamageTracks $rw.DamageTrack $t.DamageTrack
        
        # Weighted scoring: name (50%), damage (40%), type match (10%)
        $score = 0
        if ($nameScore -gt 70) {
            $score = 100 + $damageScore  # Exact/close name match gets priority
        } else {
            $score = ($nameScore * 0.3) + ($damageScore * 0.6)
        }
        if ($typeMatch) { $score += 10 }
        if (-not $typeMatch) { $score = $score * 0.3 }  # Heavy penalty for type mismatch
        
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
        }
        
        if ($matchType -eq "FF") {
            $usedFF[$bestMatch.Name] = $true
        } else {
            $usedSA[$bestMatch.Name] = $true
        }
    }
}

Write-Output "`nFound $($matches.Count) matches:"
$matches | Format-Table -AutoSize

# Save matches to JSON
$matches | ConvertTo-Json -Depth 10 | Out-File "rimworld_to_aff_matches.json" -Encoding UTF8
Write-Output "`nMatches saved to rimworld_to_aff_matches.json"

