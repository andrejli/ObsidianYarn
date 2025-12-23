import os
import json
import re
from datetime import datetime

def parse_markdown_file(filepath):
    """Parse a markdown file and extract structured data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    data = {
        'filename': os.path.basename(filepath),
        'name': '',
        'created': '',
        'author': '',
        'tags': [],
        'links': [],
        'notes': ''
    }
    
    # Extract name (first heading)
    name_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if name_match:
        data['name'] = name_match.group(1)
    
    # Extract created date
    created_match = re.search(r'\*\*Created:\*\* (.+)', content)
    if created_match:
        data['created'] = created_match.group(1)
    
    # Extract author
    author_match = re.search(r'\*\*Author:\*\* (.+)', content)
    if author_match:
        data['author'] = author_match.group(1)
    
    # Extract tags
    tags_section = re.search(r'## Tags\n(.+?)\n---', content, re.DOTALL)
    if tags_section:
        tags_text = tags_section.group(1).strip()
        data['tags'] = re.findall(r'#[\w-]+', tags_text)
    
    # Extract links
    links_section = re.search(r'## Links\n(.+?)\n---', content, re.DOTALL)
    if links_section:
        links_text = links_section.group(1).strip()
        data['links'] = re.findall(r'\[\[([^\]]+)\]\]', links_text)
    
    # Extract notes section
    notes_section = re.search(r'## Notes\n(.+?)$', content, re.DOTALL)
    if notes_section:
        data['notes'] = notes_section.group(1).strip()
    
    return data

def add_comprehensive_notes(data):
    """Add comprehensive notes based on the node name."""
    name = data['name']
    notes_map = {
        'SarajevoAssassination': 'The assassination of Archduke Franz Ferdinand of Austria and his wife Sophie in Sarajevo on June 28, 1914. This event is widely considered the trigger that set off World War I. The attack was carried out by Gavrilo Princip, a member of the Young Bosnia movement, backed by the Serbian secret society Black Hand.',
        
        'FranzFerdinand': 'Archduke Franz Ferdinand (1863-1914) was the heir presumptive to the Austro-Hungarian throne. His assassination sparked a chain of events leading to WWI. He was known for his support of federalism and greater autonomy for ethnic groups within the empire, which made him controversial among Serbian nationalists.',
        
        'SophieChotek': 'Sophie, Duchess of Hohenberg (1868-1914), wife of Archduke Franz Ferdinand. She was killed alongside her husband in the Sarajevo assassination. Her marriage to Franz Ferdinand was considered morganatic, and she faced significant social restrictions at the imperial court.',
        
        'GavriloPrincip': 'Gavrilo Princip (1894-1918) was a Bosnian Serb nationalist who assassinated Archduke Franz Ferdinand and Sophie. A member of Young Bosnia and backed by the Black Hand, he was 19 years old at the time. He was too young for the death penalty and received a 20-year sentence, dying of tuberculosis in prison in 1918.',
        
        'BlackHand': 'Officially known as "Unification or Death," the Black Hand was a secret Serbian nationalist society formed in 1901. Led by Colonel Dragutin Dimitrijević (known as Apis), it aimed to unite all South Slavic territories. The organization provided weapons, training, and support to the assassins.',
        
        'YoungBosnia': 'A revolutionary movement of predominantly Serb, but also Croat and Muslim South Slav students in Austria-Hungary who wanted to break away from the empire. Members were influenced by anarchist and nationalist ideologies. Gavrilo Princip was a key member.',
        
        'LatinBridge': 'Latin Bridge (Latinska ćuprija) is an Ottoman-era bridge over the Miljacka River in Sarajevo. It was the location where Gavrilo Princip shot Franz Ferdinand and Sophie. The spot is now marked with a memorial plaque and is a significant historical site.',
        
        'Sarajevo': 'Capital and largest city of Bosnia and Herzegovina. In 1914, it was part of the Austro-Hungarian Empire. The city had significant ethnic tensions between Serbs, Croats, and Muslims. The assassination occurred during the Archduke\'s visit to inspect military maneuvers.',
        
        'Timeline-Morning': 'June 28, 1914, 10:00 AM - The Archduke and Sophie arrived at Sarajevo railway station. The date was particularly provocative as it was St. Vitus\' Day (Vidovdan), a Serbian national holiday commemorating the Battle of Kosovo.',
        
        'Timeline-Attempt1': 'June 28, 1914, 10:15 AM - The first assassination attempt by Nedeljko Čabrinović, who threw a bomb at the Archduke\'s car. The bomb bounced off and exploded under the next car, injuring several people. Čabrinović attempted suicide by jumping into the river but was captured.',
        
        'Timeline-CityHall': 'June 28, 1914, 10:45 AM - After the bomb attempt, the motorcade proceeded to City Hall where Franz Ferdinand gave a speech. He was visibly angry about the attack. A decision was made to change the route to visit the wounded at the hospital.',
        
        'Timeline-FatalMoment': 'June 28, 1914, 11:15 AM - At Latin Bridge, the driver took a wrong turn. While reversing, the car stalled directly in front of Gavrilo Princip, who fired two shots from about 5 feet away. Both Franz Ferdinand and Sophie were fatally wounded.',
        
        'Weapon': 'Browning M1910 semi-automatic pistol, serial number M19074, caliber .380 ACP (9×17mm). The weapon was provided by the Black Hand organization. After the assassination, it became key evidence and is now displayed in the Museum of Military History in Vienna.',
        
        'FatalShot': 'Gavrilo Princip fired two shots. The first hit Sophie in the abdomen, and the second struck Franz Ferdinand in the neck, severing his jugular vein. Sophie died almost immediately, while Franz Ferdinand died about 10 minutes later. His last words were reportedly "Sophie, Sophie, don\'t die. Stay alive for the children."',
        
        'Aftermath': 'The assassination led directly to World War I through a complex web of alliances and diplomatic failures. Austria-Hungary, backed by Germany, issued an ultimatum to Serbia. When Serbia\'s response was deemed insufficient, Austria-Hungary declared war on July 28, 1914, exactly one month after the assassination.',
        
        'JulyUltimatum': 'On July 23, 1914, Austria-Hungary delivered a 10-point ultimatum to Serbia with a 48-hour deadline. The demands were intentionally harsh and designed to be unacceptable, including allowing Austro-Hungarian officials to participate in the investigation on Serbian soil. Serbia accepted most points but rejected those violating its sovereignty.',
        
        'AustriaDeclaresWar': 'On July 28, 1914, exactly one month after the assassination, Austria-Hungary declared war on Serbia. This activated a chain of alliance commitments: Russia mobilized to support Serbia, Germany declared war on Russia, France entered to support Russia, and Germany invaded Belgium, bringing Britain into the war.',
        
        'WWI': 'World War I (1914-1918) resulted in over 16 million deaths and 21 million wounded. It ended with the collapse of four empires: Austro-Hungarian, Ottoman, Russian, and German. The Treaty of Versailles and other peace settlements reshaped Europe\'s political map and set the stage for WWII.',
        
        'Trial': 'The trial of the conspirators began on October 12, 1914, in Sarajevo. Twenty-five defendants were charged. The proceedings were conducted in German, which many defendants didn\'t speak well. The trial was widely criticized as being politically motivated rather than seeking true justice.',
        
        'Verdict': 'Gavrilo Princip was found guilty on October 28, 1914. Because he was under 20 years old at the time of the assassination, he could not be sentenced to death under Austro-Hungarian law. He received the maximum sentence of 20 years in prison. Three other conspirators received death sentences and were executed.',
        
        '1914-06-28': 'June 28, 1914 - A date that changed world history. Also known as Vidovdan (St. Vitus\' Day), this Serbian national holiday commemorates the 1389 Battle of Kosovo. The choice of this date for the Archduke\'s visit was seen as provocative by Serbian nationalists.',
        
        'AustriaHungary': 'The Austro-Hungarian Empire was a constitutional union between Austria and Hungary from 1867 to 1918. It was a multi-ethnic state with significant tensions between different nationalities. The empire collapsed at the end of WWI and was divided into several new nations.',
        
        'Prison': 'Gavrilo Princip was imprisoned at Theresienstadt fortress (now Terezín, Czech Republic). Conditions were harsh, and his health deteriorated rapidly. He suffered from tuberculosis of the bone, which led to the amputation of his right arm. He died on April 28, 1918, at age 23, just months before the war ended.'
    }
    
    if name in notes_map:
        data['notes'] = notes_map[name]
    
    return data

def export_to_json(input_dir, output_file):
    """Export all markdown files to a structured JSON file."""
    nodes = []
    
    # Get all markdown files
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    
    print(f"Processing {len(md_files)} markdown files...")
    
    for md_file in md_files:
        filepath = os.path.join(input_dir, md_file)
        try:
            data = parse_markdown_file(filepath)
            data = add_comprehensive_notes(data)
            nodes.append(data)
            print(f"  Processed: {md_file}")
        except Exception as e:
            print(f"  Error processing {md_file}: {e}")
    
    # Create the final structure
    output = {
        'metadata': {
            'exported_at': datetime.now().isoformat(),
            'total_nodes': len(nodes),
            'source_directory': input_dir
        },
        'nodes': nodes,
        'graph_statistics': {
            'total_links': sum(len(n['links']) for n in nodes),
            'total_tags': len(set(tag for n in nodes for tag in n['tags'])),
            'unique_tags': sorted(list(set(tag for n in nodes for tag in n['tags'])))
        }
    }
    
    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Exported {len(nodes)} nodes to {output_file}")
    print(f"  Total links: {output['graph_statistics']['total_links']}")
    print(f"  Unique tags: {output['graph_statistics']['total_tags']}")

if __name__ == "__main__":
    input_directory = os.path.join(os.getcwd(), "GENERATED_MARKDOWN")
    output_filename = "sarajevo_assassination_graph.json"
    
    export_to_json(input_directory, output_filename)
