JOB 1
=====
In the first Map reduce we calculate the term frequency for each token, grouped by the category

MAP 
---
**INPUT** : articles

**Pseudocode:**
```
foreach article in articles:
	article.categories = [cat1, cat2,...]
	foreach token in article
		td = token frequency in article
		 emit (token, {category:article.categories, termfreq:td})
```
 **OUTPUT**
 ```
 ('screw', [
		{categories:['tools', 'devices'], termfreq:10}
		{categories:['handheld tools', 'tools'], termfreq:5}
		.....
)
```
REDUCE 
---
Collect all the categories and sum them up

 **INPUT**
 
 ```
 ('screw', [
		{categories:['tools', 'devices'], termfreq:10}
		{categories:['handheld tools', 'tools'], termfreq:5}
		.....
)
```

**OUTPUT**

```
[{'screw':{
		'tools':15,
		'devices':10,
		'handheld tools':5,
		....
	}
},
...........
]
```

JOB 2
====
From the output of **JOB 1**, calculate the td-idf for each token for each category


**INPUT**
```
[{'screw':{
		'tools':15,
		'devices':10,
		'handheld tools':5,
		....
	}
},
...........
]
```
**OUTPUT**
```
[{'screw':{
		'tools':0.8,
		'devices':0.9,
		'handheld tools':0.5,
		....
	}
},
...........
]
```

Search Problem:
================
For a given Patent, find the wikipedia category that best describe that patent
```
foreach token in patent
    tokens[token] = [cat1, cat2] # By looking up keys from output of JOB2

## Some algorithm/heuristics to find the most relevant categories from the 'tokens' array
    
    
```


