# IN104 - Rapport du projet Hanabi

Auteurs : Atoli Huppe, Guillaume Yon

[Dépôt de notre groupe](https://github.com/AtoliH/hanabi)



## Stratégie retenue

Mise en place de la stratégie de recommandation

## Points techniques

La première question importante que nous nous sommes posée est celle du stockage des informations : quelle structure était la plus adaptée pour mémoriser les recommandations, les actions possibles pour chaque joueur... ?
Notre choix s'est basé sur la "durée de vie" de ces informations : les actions réalisables par un joueur sont remises à jour dès qu'on passe au joueur suivant, mais les recommandations restent les mêmes tant qu'un nouvel indice n'a pas été donné. De plus , l'indice du joueur courant étant toujours 0, il fallait une structure qui ne prenne pas des entiers en indice. 

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
S'est posé également un problème pour retrouver le nom du joueur courant, puisque la variable `game.current_player_name` contient un objet qui ressemble à `\x1b[1mAlice\x1b[0m`

## Tests unitaires ou de non-régression

Présentez quelques (disons 2) tests unitaires.
Dans l'idéal, pour celles et ceux qui sont tombés sur un (gros) bug qui leur a pris du temps, il devrait y avoir un test unitaire qui protège contre sa réapparition.

Exemple :

- Le test `game_42.py` replace la partie dans une situation où l'AI est obligée de défausser une carte précieuse ; je veux garantir que c'est le 5 vert parce que celle celui qui fait perdre le moins de points.

- Le test `fin_de_partie.py` vérifie que les noms des joueurs sont les bons sur le dernier tour de jeu, parce que dans [telle situation...] ça n'avait pas été le cas.



## Tests en série - statistiques - analyse des résultats

C'est le morceau le plus important de ce rapport.

### AI Cheater

Le script `son_nom.py` lance l'AI 10000 fois.

Le score moyen obtenu est [...] ; pour comparaison le Cheater de l'article fait en moyenne 24.87.

Voici l'histogramme de nos résultats :
![Histogramme de l'AI Cheater](images/mon_histogramme.png)

à comparer avec celui (c) de l'article :
![Les 3 histogrammes de l'article](images/histogrames_hatstrat.png)



Important : pensez à analyser et discuter les différences entre vos résultats et l'article.
En particulier, si vous faites mieux ou moins bien, quelles en sont les raisons, et des pistes d'amélioration.
Les parties qui finissent à moins de 25 points sont aussi intéressantes à analyser.


### AI Recommendation

Idem, expliquez ce que vous avez fait pour cette 2e AI.


## Conclusion et perspectives

Parce qu'il est toujours bon d'aider son lecteur à retenir les points importants,
et lui donner des nouvelles pistes de réflexion.
