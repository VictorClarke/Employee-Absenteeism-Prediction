
drop database if exists predicted_outputs;
create database if not exists predicted_outputs;

use predicted_outputs;

drop table if exists predicted_outputs;
create table predicted_outputs (
reason1 bit not null,
reason2 bit not null,
reason3 bit not null,
month_value int not null,
transportation_expense int not null,
age int not null,
body_mass_index int not null, 
education bit not null,
children int not null, 
pets int not null, 
probability float not null, 
prediction bit not null
);

ALTER TABLE predicted_outputs
ADD COLUMN reason4 bit not null AFTER reason3;

select *  from predicted_outputs;

