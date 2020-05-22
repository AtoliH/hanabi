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
S'est posé également un problème pour retrouver le nom du joueur courant, puisque la variable `game.current_player_name` contient un objet qui ressemble à `\x1b[1mAlice\x1b[0m` et qui n'est donc pas une chaîne de caractères. Nous avons utilisé la syntaxe `game.current_player_name[4:-4]` pour retrouver une chaîne de caractères. 

## Tests unitaires ou de non-régression

Pas de tests unitaires pour le moment. 



## Tests en série - statistiques - analyse des résultats

C'est le morceau le plus important de ce rapport.


### AI Recommendation

Idem, expliquez ce que vous avez fait pour cette 2e AI.


### AI Information

Le script `stats_information_ai.py` lance le robot 1000 fois. 
Pour le moment, le score moyen obtenu est 23.3. Par comparaison, celui de l'article réalise un score moyen de 24.68. 

![Histogramme de la stratégie de recommandation](https://github.com/AtoliH/hanabi/blob/Guillaume/src/hanabi/stats_information_ai.png)

Dans notre programme, les joueurs prennent leur décision uniquement à partir des informations publiques, connues de tous les joueurs. Ils pourraient toutefois améliorer les informations qu'ils possèdent en utilisant des déductions privées, c'est-à-dire qu'ils sont les seuls à pouvoir faire, à partir notamment des mains des autres joueurs. 

Le calcul de la carte qui a la plus grande probabilité d'être jouable est simplifié : on estime la probabilité en effectuant le rapport du nombre de possibilités jouables sur le nombre total de possibilités. Mais les auteurs de l'article évoquent un calcul plus abouti, qui prend en compte le nombre de cartes de chaque type, et qui permet un meilleur ciblage des cartes. 


Ceci peut expliquer les performances moindres de notre programme. 



## Conclusion et perspectives

Parce qu'il est toujours bon d'aider son lecteur à retenir les points importants,
et lui donner des nouvelles pistes de réflexion.
