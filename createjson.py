import json

def parse_amazon_meta_to_json(file_path):
    products = []
    product = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Id:'):
                if product:  
                    products.append(product)
                product = {"Id": int(line.split()[1].strip())}
            elif line.startswith('ASIN:'):
                product['ASIN'] = line.split()[1].strip()
            elif line.startswith('title:'):
                product['title'] = line[len('title:'):].strip()
            elif line.startswith('group:'):
                product['group'] = line[len('group:'):].strip()
            elif line.startswith('salesrank:'):
                product['salesrank'] = int(line.split()[1].strip())
            elif line.startswith('similar:'):
                product['similar'] = line[len('similar:'):].strip().split()
            elif line.startswith('categories:'):
                product['categories'] = ''
                continue  
            elif line.startswith('reviews:'):
                product['reviews'] = line[len('reviews:'):].strip()
                continue  
            elif '|' in line:
                if 'categories' in product and 'reviews' not in product:
                    product['categories'] += line + ' '
            elif 'cutomer:' in line:
                if 'reviews' in product:
                    product['reviews'] += line + ' '

        if product:  
            products.append(product)

    return products

if __name__ == '__main__':
    file_path = '/Users/spencer/Desktop/CS-458-Fall-2023/Amazon Final Project/txt/amazon-meta.txt'
    products = parse_amazon_meta_to_json(file_path)


    with open('amazon-meta.json', 'w', encoding='utf-8') as json_file:
        json.dump(products, json_file, ensure_ascii=False, indent=4)
