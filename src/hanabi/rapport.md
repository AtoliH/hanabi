# IN104 - Rapport du projet Hanabi

Auteurs : Atoli Huppe, Guillaume Yon

[Dépôt de notre groupe](https://github.com/AtoliH/hanabi)



## Stratégie retenue

Mise en place de la stratégie de recommandation

## Points techniques

La première question importante que nous nous sommes posée est celle du stockage des informations : quelle structure était la plus adaptée pour mémoriser les recommandations, les actions possibles pour chaque joueur... ?
Notre choix s'est basé sur la "durée de vie" de ces informations : les actions réalisables par un joueur sont remises à jour dès qu'on passe au joueur suivant, mais les recommandations restent les mêmes tant qu'un nouvel indice n'a pas été donné. De plus, l'indice du joueur courant étant toujours 0, il fallait une structure qui ne prenne pas des entiers en indice. 

Pour répondre à ces exigences, nous avons choisi d'utiliser des dictionnaires et de les passer en attributs de notre robot. 



```python
    def __init__(self, game):
        hanabi.ai.AI.__init__(self, game)

        self.recommandation_list = {}
        self.played_cards = {}

        for player_name in self.game.players:
            self.recommandation_list[player_name] = " "
            self.played_cards[player_name] = 0
```

La stratégie d'information a posé un autre problème, celui de l'attribution des tables de possibilités. En effet, à chaque fois qu'un joueur sort une carte de sa main, la nouvelle carte piochée est ajoutée à la fin de la main du joueur. Il faut donc réaffecter les tables, puisque les cartes ont changé de position :

```python 
	if action[0] != 'c' : # Si on a joué ou défaussé une carte, il faut réattribuer les tables de possibilités
            for a in range(3):

                if a < index :
                    new_table[a] = self.tables[current_player_name][a]
                else : 
                    new_table[a] = self.tables[current_player_name][a + 1]

            self.tables[current_player_name] = new_table.copy()
```


## Tests unitaires ou de non-régression

Une batterie des tests unitaire a été écrite afin de prévenir la régression du comportement de l'IA Recommandation vis à vis des indices qu'elle donne. On s'assure ainsi que la priorité des actions a effectuer est bien respectée. Par exemple si une carte de rang 5 peut être jouée celle-ci doit être jouée.




## Tests en série - statistiques - analyse des résultats

C'est le morceau le plus important de ce rapport.


### AI Recommendation

Le score moyen obtenu par cette IA est 22,2. Ce score est proche de celui obtenu dans l'article mais reste légèrement moindre pour des raisons que l'on ignore.

![Histogramme de la stratégie de recommandation](https://github.com/AtoliH/hanabi/blob/Guillaume/src/hanabi/stats_recommandation_ai.png)

L'IA base ses actions sur des indices donnés par les autres joueurs suivant un code prédéterminé. Donner un indice de valeur ou de couleur a tel ou tel joueur a une certaine signification autre que simplement l'indice donné.


### AI Information

Le script `stats_information_ai.py` lance le robot 1000 fois. 
Pour le moment, le score moyen obtenu est 23.3. Par comparaison, celui de l'article réalise un score moyen de 24.68. 

![Histogramme de la stratégie de l'information](https://github.com/AtoliH/hanabi/blob/Guillaume/src/hanabi/stats_information_ai.png)

Dans notre programme, les joueurs prennent leur décision uniquement à partir des informations publiques, connues de tous les joueurs. Ils pourraient toutefois améliorer les informations qu'ils possèdent en utilisant des déductions privées, c'est-à-dire qu'ils sont les seuls à pouvoir faire, à partir notamment des mains des autres joueurs. 

Le calcul de la carte qui a la plus grande probabilité d'être jouable est simplifié : on estime la probabilité en effectuant le rapport du nombre de possibilités jouables sur le nombre total de possibilités. Mais les auteurs de l'article évoquent un calcul plus abouti, qui prend en compte le nombre de cartes de chaque type, et qui permet un meilleur ciblage des cartes. 


Ceci peut expliquer les performances moindres de notre programme. 



## Conclusion et perspectives

Parce qu'il est toujours bon d'aider son lecteur à retenir les points importants,
et lui donner des nouvelles pistes de réflexion.
