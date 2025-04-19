<style>  
b { color: #459FF2 }
o { color:rgb(7, 246, 75) }
r { color: #B57D39 }
</style>
# problem 1 - Grid City

Consider an infinite city consisting of locations $(x,y)$ where $x, y$ are integers.
  From each location $(x,y)$, one can go east, west, north, or south. 
  These movements are what we refer to as ‘actions’. 
  Specifically, an action is a change in the (x, y) coordinates: (+1, 0) represents moving east, (-1, 0) 
  represents moving west, (0, +1) represents moving north, and (0, -1) represents moving south.
  \\
  \\
  You start at $(0,0)$ and want to go to $(m, n)$, where $m, n \geq 0$.
  We can define the following search problem to capture this:

$s_\text{start} = (0,0)$

$\text{Actions}(s) = \{ (+1, 0), (-1, 0), (0, +1), (0, -1) \}$\
$\text{Succ}(s, a) = s + a$\
$\text{Cost}((x,y), a) = 1 + \max(x, 0)$ (i.e., it is more expensive as $x$ increases)\
$\text{IsEnd}(s) = \mathbf{1}[s = (m,n)]$

 What is the minimum cost of reaching location $(m,n)$ (note that $m,n \geq 0$) starting from location $(0,0)$ in the above city? Describe one possible path achieving the minimum cost.  Is it unique (i.e., are there multiple paths that achieve the minimum cost)? Note that the cost of the actions depends on the x-coordinate of the current state.
 ## Expected 
<r>{Provide an expression for the minimum cost. In addition, please provide 1 - 2 sentences describing one possible minimum cost path and state whether it is unique.}</r>
## mysolution

Formal expression to recursively traverse all actions and grid positions is described as:
$$
\begin{align*}
    minCost(s) &=
    \begin{cases}
        0 &\text{if } IsEnd(s) \\
        min_{a \in Actions} [Cost(s, a) + minCost(Succ, a)] &\text{Otherwise}
    \end{cases}
\end{align*}
$$

Cost of any grid $(x,y)$ is only a factor of $x$ coordinate, therefore, if we make progress in x-direction first, this cost gets added to all future costs. Since cost of going in any $y$ direction for a given $x$ is the same,  minimum cost path is traversed first from $(0,0)$ to $(0,n)$ and then from $(0,n)$ to $(m,n)$.

This minCost path is unique.

We must traverse minimum n grids in $y$ direction to reach (m, n) and minimum $m$ grids in $x$ direction.

<o>Question: we need to give  formula as in form of futureCost ?

$minCost =  n + \frac{m * (m+1)}{2}$
</o>

 ### (b) How will Uniform Cost Search (UCS) behave on this problem? Mark the following as true or false:
 \begin{enumerate}[label=\arabic*.]
     \item UCS will never terminate because the number of states is infinite.
    \item UCS will return the minimum cost path and explore only locations between $(0,0)$ and $(m,n)$; that is, $(x,y)$ such that $0 \le x \le m$ and $0 \le y \le n$
    \item UCS will return the minimum cost path and explore only locations whose past costs are less than or equal to the minimum cost from $(0,0)$ to $(m,n)$.
 \end{enumerate}
 Ans: T, F, F

 (c) Ans: F, ??, T
<a> does the graph change?</a> 

### question 2-b
I tried several start and end points. Three interesting observations are:
1. if I choose parking entrance to evgr_a landmark, the distance is long from left side of the campus. see screenshot.
2. If I reverse the path, then I get shorter distance parking entrance.
3. If my start/end are "amenity=parking_entrance" and "parking=underground", I got 0 distance, the code takes them as the same.

These observations are all understandable from the code implementation. But are not ideal for end user.

### part 2: Externalities
Provide 3-5 sentences describing (a) two externalities (one for
users of the route-planning system and one for other people/non-users of the system),
as well as (b) at least one potential solution to reduce the impact of these problems.
### answer

I am only replying with negative aspect of externalities from the use of route planning app.
- The non-users of the system will be subjected to negative externality pattern. They will see surge in landmark places which were quieter before the app was launched. The reason is route-planning app could route users to same landmark, causing overcrowding at that landmark and road/path congestion. For example, during lunchtime, a specific food location will see more people coming in than other cafeterias. This leads to uneven business opportunities for the services.
- The system routes based on best 'landmark' option and not ideal one. As I showed in my previous plot. This actually meant user took a longer route. This can be mitigated by using user's current location more accurately.

There are several enhancements to the app possible, A simple one could be to leverage localization radius based on current location. E.g. CS students, are routed to nearby  CS quad landmarks for most of the landmark services. This is in fact what the route planning app is supposed to do but from example, this is not the case. This enhancement will require more specific labels.
