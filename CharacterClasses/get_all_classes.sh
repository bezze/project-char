
class_list=("Barbarian" "Bard" "Cleric" "Druid" "Fighter" "Monk" "Paladin"\
    "Ranger" "Rogue" "Sorcerer" "Warlock" "Wizard")

for CLASS in ${class_list[@]}
do
curl "https://roll20.net/compendium/dnd5e/Classes:"${CLASS}"#h-"${CLASS} > $CLASS
done
