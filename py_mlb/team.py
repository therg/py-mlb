from fetcher import Fetcher
import player

class Team(dict):
    """Represents a team"""
    def __init__(self, attributes):
        """
        Constructor
        
        Arguments:
        attributes - A dict of key/value pairs used to populate the team, passed by the league information
        """
        self.roster = {}
        for key, value in attributes.iteritems():
            self[key] = value
    
    def loadRoster(self):
        """
        Calls MLB.com servers to obtain the complete roster for the team. If call fails, '_error' property is set.
        """
        f = Fetcher(Fetcher.MLB_ROSTER_URL, team_id=self['team_id'])
        j = f.fetch()
        
        if 'roster_40' not in j:
            self._error = "ERROR on %s: key roster_40 not found (cannot load 40 man roster)" % (f.url)            
            return False
        
        parent = j['roster_40']['queryResults']
        
        if parent['totalSize'] > 0:
            for record in parent['row']:
                player_id = record['player_id']
                p = player.Player(player_id)
                p.load()
                self.roster[player_id] = p


    def getPlayer(self, player_id):
        """
        Returns a player object, or None
        
        Arguments:
        player_id - The MLB.com player ID
        """
        if player_id in self.roster:
            return self.roster[player_id]

        return None
