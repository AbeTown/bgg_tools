# bgg_tools

`bgg_tools` is a package useful for working with data from [BoardGameGeek](https://www.boardgamegeek.com). It serves as a python inteface for interfacing with both games and user collections.

## Installation
Currently, installation is only possible by cloning the repo and building the pacakge locally.

    git clone https://github.com/shelmich/bgg_toos
    cd bgg_tools
    pip install -e .

## Usage

### Games

Downloading data for a single game is relatively simple, if you know the BoardGameGeek ID for the game you want (this may not be a trivial task however).

    import bgg_tools as bgg

    # Game with id=1 is Die Macher
    game = gbb.Game(id=1) 

Additionally, the game's data isn't download until called for:

    game.download_game()

If you want the ratings for the game, there is a separate function for that, as it is an intensive pull for some games, such as Catan.

    game.get_ratings()



## Goals
The goal of this toolset is to eventually facilitate an easy mechanism for doing board game recommendation, but in order to do that, I need soeme tools for pulling and working with the data.

Eventually, I would like to build a recommender system, as well as do some board game embeddings (as that sounds kinda fun).






