#!/usr/bin/python3

import json
from typing import List, Optional, Tuple
from math import radians
from copy import copy

from util import *
#from util import SearchProblem, State, UniformCostSearch
from mapUtil import (
    CityMap,
    checkValid,
    createGridMap,
    createGridMapWithCustomTags,
    createStanfordMap,
    getTotalCost,
    locationFromTag,
    printMap,
    makeGridLabel,
    makeTag,
    RADIUS_EARTH,
)
def extractPath(startLocation: str, search: SearchAlgorithm) -> List[str]:
    """
    Assumes that `solve()` has already been called on the `searchAlgorithm`.

    We extract a sequence of locations from `search.path` (see util.py to better
    understand exactly how this list gets populated).
    """
    return [startLocation] + search.actions

def printPath(
    path: List[str],
    waypointTags: List[str],
    cityMap: CityMap,
    outPath: Optional[str] = "path.json",
):
    doneWaypointTags = set()
    for location in path:
        for tag in cityMap.tags[location]:
            if tag in waypointTags:
                doneWaypointTags.add(tag)
        tagsStr = " ".join(cityMap.tags[location])
        doneTagsStr = " ".join(sorted(doneWaypointTags))
        print(f"Location {location} tags:[{tagsStr}]; done:[{doneTagsStr}]")
    print(f"Total distance: {getTotalCost(path, cityMap)}")

    # (Optional) Write path to file, for use with `visualize.py`
    if outPath is not None:
        with open(outPath, "w") as f:
            data = {"waypointTags": waypointTags, "path": path}
            json.dump(data, f, indent=2)

########################################################################################
# Problem 3a: Modeling the Waypoints Shortest Path Problem.


class WaypointsShortestPathProblem(SearchProblem):
    """
    Defines a search problem that corresponds to finding the shortest path from
    `startLocation` to any location with the specified `endTag` such that the path also
    traverses locations that cover the set of tags in `waypointTags`. Note that tags
    from the `startLocation` count towards covering the set of tags.

    Hint: naively, your `memory` representation could be a list of all locations visited.
    However, that would be too large of a state space to search over! Think
    carefully about what `memory` should represent.
    """
    def __init__(
        self, startLocation: str, waypointTags: List[str], endTag: str, cityMap: CityMap
    ):
        self.startLocation = startLocation
        self.endTag = endTag
        self.cityMap = cityMap

        # We want waypointTags to be consistent/canonical (sorted) and hashable (tuple)
        self.waypointTags = tuple(sorted(waypointTags))

    def startState(self) -> State:
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        # start state could be progress, can we maintain a state of startState
        self.done = []
        self.pending = copy(list(self.waypointTags))
        self.end_location = locationFromTag(self.endTag, self.cityMap)

        self.startState = State(self.startLocation)
        return self.startState

        # END_YOUR_CODE

    def isEnd(self, state: State) -> bool:
        # BEGIN_YOUR_CODE (our solution is 5 lines of code, but don't worry if you deviate from this)

        def match_tag(loc):
            for tag in cityMap.tags[loc]:
                if tag in self.waypointTags:
                    self.done.add(tag)
                    self.pending.remove(tag)

        match_tag(state.location)
        if state.location == self.end_location and len(self.pending) == 0:
            return True
        return False
        # END_YOUR_CODE

    def actionSuccessorsAndCosts(self, state: State) -> List[Tuple[str, State, float]]:
        # BEGIN_YOUR_CODE (our solution is 17 lines of code, but don't worry if you deviate from this)
        result = []
        for action, distance in self.cityMap.distances[state.location].items():
            result.append((label2, State(label2, memory=state), distance))
        return result
        # END_YOUR_CODE



def t_3ab(
    cityMap: CityMap,
    startLocation: str,
    endTag: str,
    waypointTags: List[str],
    expectedCost: Optional[float] = None,
):
    ucs = UniformCostSearch(verbose=1)
    problem = WaypointsShortestPathProblem(
        startLocation,
        waypointTags,
        endTag,
        cityMap,
    )
    ucs.solve(problem)
    path = extractPath(startLocation, ucs)
    checkValid(path, cityMap, startLocation, endTag, waypointTags)


cityMap=createGridMap(3, 5),
startLocation=makeGridLabel(0, 0),
waypointTags=[makeTag("y", 4)],
endTag=makeTag("label", makeGridLabel(2, 2)),
expectedCost=8,

t_3ab(cityMap, startLocation,waypointTags, endTag)
