import os
import json

def combine_files(source_folder, results_folder):
    os.makedirs(results_folder)

    for name in os.listdir(source_folder):
        curr_folder = os.path.join(source_folder, name)
        combined_contents = []

        for f in os.listdir(curr_folder):
            with open(os.path.join(source_folder, name, f), 'r', encoding='utf-8') as infile:
                combined_contents.append(json.load(infile))

        with open(os.path.join(results_folder, f'{name}.json'), 'w+', encoding='utf-8') as outfile:
            json.dump(combined_contents, outfile, ensure_ascii=False)