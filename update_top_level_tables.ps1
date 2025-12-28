# Update top-level weapons and armor tables with all Vanilla Expanded items
$processed = Get-Content "F:\Python Apps\EPIC\vanilla_expanded_processed.json" | ConvertFrom-Json

function Sanitize-Link {
    param($name, $mod)
    $name = $name -replace '[<>:"/\\|?*]', ''
    $name = $name -replace '\s+', '-'
    
    $modPath = switch ($mod) {
        "Vanilla Weapons Expanded" { "Vanilla-Weapons-Expanded" }
        "Vanilla Weapons Expanded - Laser" { "Vanilla-Weapons-Expanded\Laser" }
        "Vanilla Weapons Expanded - Grenades" { "Vanilla-Weapons-Expanded\Grenades" }
        "Vanilla Weapons Expanded - Heavy Weapons" { "Vanilla-Weapons-Expanded\Heavy-Weapons" }
        "Vanilla Weapons Expanded - Coilguns" { "Vanilla-Weapons-Expanded\Coilguns" }
        "Vanilla Weapons Expanded - Makeshift" { "Vanilla-Weapons-Expanded\Makeshift" }
        "Vanilla Weapons Expanded - Frontier" { "Vanilla-Weapons-Expanded\Frontier" }
        "Vanilla Weapons Expanded - Non-Lethal" { "Vanilla-Weapons-Expanded\Non-Lethal" }
        "Vanilla Weapons Expanded - Tribal" { "Vanilla-Weapons-Expanded\Tribal" }
        "Vanilla Persona Weapons Expanded" { "Vanilla-Weapons-Expanded\Persona-Weapons" }
        "Vanilla Factions Expanded - Settlers" { "Vanilla-Factions-Expanded\Settlers" }
        "Vanilla Factions Expanded - Ancients" { "Vanilla-Factions-Expanded\Ancients" }
        "Vanilla Factions Expanded - Pirates" { "Vanilla-Factions-Expanded\Pirates" }
        "Vanilla Factions Expanded - Classical" { "Vanilla-Factions-Expanded\Classical" }
        default { "" }
    }
    
    return "[[Weapons/Rimworld/$modPath/$name\|$($name -replace '-', ' ')]]"
}

function Sanitize-ArmorLink {
    param($name, $mod)
    $name = $name -replace '[<>:"/\\|?*]', ''
    $name = $name -replace '\s+', '-'
    
    $modPath = switch ($mod) {
        "Vanilla Armour Expanded" { "Vanilla-Armor-Expanded" }
        "Vanilla Apparel Expanded" { "Vanilla-Armor-Expanded\Apparel" }
        "Vanilla Apparel Expanded - Accessories" { "Vanilla-Armor-Expanded\Accessories" }
        default { "" }
    }
    
    return "[[Armor/Rimworld/$modPath/$name\|$($name -replace '-', ' ')]]"
}

# Organize weapons by mod
$weaponsByMod = @{}
foreach ($weapon in $processed.weapons) {
    if (-not $weaponsByMod.ContainsKey($weapon.mod)) {
        $weaponsByMod[$weapon.mod] = @()
    }
    $weaponsByMod[$weapon.mod] += $weapon
}

# Organize armor by mod
$armorsByMod = @{}
foreach ($armor in $processed.armors) {
    if (-not $armorsByMod.ContainsKey($armor.mod)) {
        $armorsByMod[$armor.mod] = @()
    }
    $armorsByMod[$armor.mod] += $armor
}

# Generate weapon tables
Write-Host "`n=== WEAPON TABLES ===" -ForegroundColor Green
foreach ($mod in $weaponsByMod.Keys | Sort-Object) {
    $weapons = $weaponsByMod[$mod]
    $meleeWeapons = $weapons | Where-Object { $_.isMelee }
    $rangedWeapons = $weapons | Where-Object { -not $_.isMelee }
    
    Write-Host "`n### $mod" -ForegroundColor Yellow
    
    if ($meleeWeapons.Count -gt 0) {
        Write-Host "`n**Melee Weapons:**"
        Write-Host ""
        Write-Host "| Weapon | 1 | 2 | 3 | 4 | 5 | 6 | 7+ |"
        Write-Host "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
        foreach ($w in $meleeWeapons | Sort-Object label) {
            $link = Sanitize-Link $w.label $mod
            $track = $w.affDamageTrack
            Write-Host "| $link | $($track[0]) | $($track[1]) | $($track[2]) | $($track[3]) | $($track[4]) | $($track[5]) | $($track[6]) |"
        }
    }
    
    if ($rangedWeapons.Count -gt 0) {
        if ($mod -like "*Pirates*") {
            Write-Host "`n**Warcasket Ranged Weapons (Vehicle-Scale):**"
        } else {
            Write-Host "`n**Ranged Weapons:**"
        }
        Write-Host ""
        Write-Host "| Weapon | 1 | 2 | 3 | 4 | 5 | 6 | 7+ |"
        Write-Host "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
        foreach ($w in $rangedWeapons | Sort-Object label) {
            $link = Sanitize-Link $w.label $mod
            $track = $w.affDamageTrack
            Write-Host "| $link | $($track[0]) | $($track[1]) | $($track[2]) | $($track[3]) | $($track[4]) | $($track[5]) | $($track[6]) |"
        }
    }
}

# Generate armor tables
Write-Host "`n`n=== ARMOR TABLES ===" -ForegroundColor Green
foreach ($mod in $armorsByMod.Keys | Sort-Object) {
    $armors = $armorsByMod[$mod]
    
    Write-Host "`n### $mod" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "| Armor | 1 | 2 | 3 | 4 | 5 | 6 | 7+ |"
    Write-Host "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    foreach ($a in $armors | Sort-Object label) {
        $link = Sanitize-ArmorLink $a.label $a.mod
        # Calculate protection track
        $maxArmor = [Math]::Max($a.sharpArmor, [Math]::Max($a.bluntArmor, $a.heatArmor))
        $affTrack = @(0,0,0,0,0,0,1)
        if ($maxArmor -le 0.1) { $affTrack = @(0,0,0,0,0,0,1) }
        elseif ($maxArmor -le 0.2) { $affTrack = @(0,0,0,0,0,1,1) }
        elseif ($maxArmor -le 0.3) { $affTrack = @(0,0,0,0,1,1,2) }
        elseif ($maxArmor -le 0.4) { $affTrack = @(0,0,0,1,1,2,2) }
        elseif ($maxArmor -le 0.5) { $affTrack = @(0,0,1,1,2,2,3) }
        elseif ($maxArmor -le 0.6) { $affTrack = @(0,1,1,2,2,3,3) }
        elseif ($maxArmor -le 0.7) { $affTrack = @(0,1,1,2,2,3,4) }
        elseif ($maxArmor -le 0.8) { $affTrack = @(1,1,2,2,3,4,5) }
        else { $affTrack = @(1,2,2,3,3,4,5) }
        Write-Host "| $link | $($affTrack[0]) | $($affTrack[1]) | $($affTrack[2]) | $($affTrack[3]) | $($affTrack[4]) | $($affTrack[5]) | $($affTrack[6]) |"
    }
}

Write-Host "`n`nTables generated! Copy the output above to the top-level files." -ForegroundColor Cyan



