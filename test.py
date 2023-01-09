import pendulum
from evalidate import safeeval, EvalException

now = pendulum.now()
d=now
data={'d':now}

try:
    result=safeeval("d.week_of_year==2",data, addnodes=['Attribute', 'Call'], attrs=['day', 'week_of_year', 'now'])
except EvalException as e:
    print(e)
    result=False

print(d,result)

...