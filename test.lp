#script (python)
import clingo
import subprocess
import string

#const istop  = "SAT".
#const imin   = 1.

#include<incmode>.

def get(val, default):
    return val if val != None else default

def main(prg):
	imin   = get(prg.get_const("imin"), clingo.Number(0))
	imax   = prg.get_const("imax")
	istop  = get(prg.get_const("istop"), clingo.String("SAT"))

	step, ret = 0, None
        
	while ((imax is None or step < imax.number) and (step == 0   or step < imin.number or ((istop == "SAT" and not ret.satisfiable) or (istop == "UNSAT"   and not ret.unsatisfiable) or (istop == "UNKNOWN" and not ret.unknown)))):
           
		
		parts = []
		parts.append(("check", [step]))
		if step > 0:
			prg.release_external(clingo.Function("query", [step-1]))
			parts.append(("step", [step]))
			prg.cleanup()
		else:
			parts.append(("base", []))

		prg.ground(parts)
		prg.assign_external(clingo.Function("query", [step]), True)
		#print "=== Release external query(" + str(step) + ")   "
		ret, step = prg.solve(), step+1
    
    

#end.

#const istop  = "SAT".
#const imin   = 1.
#const imax   = 30.
#const ordering = 1.

%agentnum(C) :- C= #count{AID: agent(AID,_,_)}. 
1 {goal(TID, SERVER, AID, GOAL, 0) : agent(AID, SERVER, _, TYPE) }1 :- task(TID, SERVER, GROUP, GOAL, TYPE).


#program base.
at(ID, X, 0):- agent(ID, _, X, _).



#program check(t). 
#external query(t).


%goalstate

:- not done(TID, t), goal(TID, _, AID, GOAL, _), query(t).





#program step(t).

%used to track goal state
done(TID, t) :- at(AID, X, t), goal(TID, _, AID, X, _), agent(AID,_,_,_).
done(TID, t) :- done(TID, t-1), goal(TID, _, AID, X, _), agent(AID,_,_,_), vertice(Z, X).

done(TID, t) :- at_border(AID, X, t), goal(TID, _, AID, GOAL, _), agent(AID,_,_,_), not vertice(_, GOAL).




%border information
at_border(ID, X, t) :- at(ID, X, t), edge(_, X, Y), vertice(QUAD1, X), not vertice(QUAD1,Y), agent(ID,_,_,_).
crossed_border(ID, X, t) :- at(ID, X, t), at(ID, Y, t-1), vertice(QUAD1, X), vertice(QUAD2, Y), QUAD1!=QUAD2, agent(ID,_,_,_). 

out_of_scope(X, t) :- goal(TID, _, AID, X, _), not vertice(_, X).
 
%agents who are ready to swap quadrants
swap(TID, SERVER, AID, GOAL, GROUP, Y, DSERVER, t) :- done(TID,t), at_border(AID, X, t), goal(TID, SERVER, AID, GOAL, _), agent(AID,SERVER,_,GROUP), not vertice(_, GOAL), not vertice(_, Y), edge(DSERVER, X, Y).


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
%#show goal/5.
#show move/4.
#show query/1.
%#show at_border/3.
%#show done/2.
%#show crossed_border/3.
%#show out_of_scope/2.
#show swap/8.




 
