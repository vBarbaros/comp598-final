### Collected time of the json files
```
(venv) $ python src/collect_newest.py -o concordia.json -s concordia
(venv) $ python src/collect_newest.py -o mcgill.json -s mcgill      
(venv) $ date                                                       
Fri Nov  5 20:46:11 EDT 2021
```

### code-book used
Given the ambiguity of some titles, especially in te case of course-related topics, 
we came up with some rules of thumb for the annotation process:

`c (course-related)` - only title text that specifically contains a course name and/or number; the title 
may contain Professor names with the condition that it's associated to a specific course;
- what IS NOT a course-related title and should be flagged us `o`:
  - text containing course management operations (admission, enrollment, withdrawal, etc) with no course number/name
  - text referring to semester or courses as a general topic with no specific topic course mentioned
  - text containing words such as `research`, or `project` which can be related to any course
  - text referring to broad science domains, i.e `neuroscience`
  - text referring to instructors/academic stuff members only, with no reference to a course

`f - (food-related)` - only title text that has a specific reference to food products that can be eaten (`Cloudberry`) 
or locations mainly used for buying (`groceries`) and/or eating (`bars`, `restaurants`);

NOTE - actually Cloudberry is a false-positive annotation for `food-related` flag 
(if we check the actual reddit post), but we need to stick to the code-book :) and this shows the 
ambiguity we might need to deal with when doing manual annotation.

`r - (residence-related)` - only title text that has a specific reference to a place to live, 
house, or student residence and anything related to these topics (prices, quality, places, addresses ,etc);
- what IS NOT a residence-related title and should be flagged us `o`:
  - text containing residence status from immigration perspective
  
`o - (other)` - everything that cannot be assigned to the previous three labels 