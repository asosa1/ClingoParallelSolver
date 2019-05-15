#const istop  = "SAT".
#const imin   = 1.

#include<incmode>.

%agentnum(C) :- C= #count{AID: agent(AID,_,_)}. 
1 {goal(TID, SERVER, AID, GOAL, 0, GSERVER) : agent(AID, SERVER, _, TYPE) }1 :- task(TID, SERVER, GSERVER, GROUP, GOAL, TYPE).


#program base.
at(ID, X, 0):- agent(ID, _, X, _).



#program check(t). 


%goalstate

:- not done(TID, t), goal(TID, _, AID, GOAL, _, _), query(t).





#program step(t).

%used to track goal state
done(TID, t) :- at(AID, X, t), goal(TID, _, AID, X, _, _), agent(AID,_,_,_).
done(TID, t) :- done(TID, t-1), goal(TID, _, AID, X, _, _), agent(AID,_,_,_), vertice(Z, X).

done(TID, t) :- at_border(AID, X, t), goal(TID, _, AID, GOAL, _, _), agent(AID,_,_,_), not vertice(_, GOAL).




%border information
at_border(ID, X, t) :- at(ID, X, t), edge(D, X, Y), vertice(QUAD1, X), not vertice(QUAD1,Y), agent(ID,_,_,_), goal(_, _, ID, _, _, D).


out_of_scope(X, t) :- goal(TID, _, AID, X, _, _), not vertice(_, X).
 
%agents who are ready to swap quadrants
swap(TID, SERVER, AID, GOAL, GROUP, Y, DSERVER, GSERVER, t) :- done(TID,t), at_border(AID, X, t), goal(TID, SERVER, AID, GOAL, _, GSERVER), agent(AID,SERVER,_,GROUP), not vertice(_, GOAL), not vertice(_, Y), edge(DSERVER, X, Y).


at(ID, Y, t) :- move(ID, X, Y, t). 
at(Y, L, t)  :-  at(Y, L, t), stay(Y, L, t-1).

:-at(ID1, Y, t), at(ID2, Y, t), ID1!=ID2.

%action genertation
1{move(ID, X, Y, t) : edge(_, X, Y); stay(ID, X, t): vertice(QUAD, X) }agentnum :-agent(ID,_,_,_), at(ID, X, t-1).



%action constraints
:- at(ID, X, t), at(ID, Y, t), X!=Y.
:-move(ID, X, Y, t), move(ID, Y, Z, t).
:-move(ID, X, Y, t), move(ID, W, Z, t), X!=W, Y!=Z.






%#show task/5.
%#show at/3.
#show agent/4.
%#show goal/6.
#show move/4.
#show query/1.
%#show at_border/3.
%#show done/2.
%#show crossed_border/3.
%#show out_of_scope/2.
#show swap/9.



