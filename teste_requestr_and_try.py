usuarios = [
    {'nome': 'ped', 'like': 20, 'post': 'Hoje é meu primeiro dia como dev jurnio'},
    {'nome': 'p2', 'like': 10, 'post': 'Hoje é meu primeiro dia como dev senior'},
    {'nome': 'p3', 'like': 30, 'post': 'Hoje é meu primeiro dia como dev contratado estou muito feliz'},

]

novos_produtos = [{**produto, 'like': produto['like'] } for produto in usuarios if( produto['like'] >= 25 ) ]

for p in novos_produtos:
    print(f'O Post mais curtido e: {p}')
