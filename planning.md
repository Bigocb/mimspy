from io import StringIO

## Goals
- Take in text and add a topic, and tags. Classification
- On returning results from a search return the results as a list of interactions and a summary of them.

## Data Structure

The central core of the system is an interaction. This will be saved to the DB. 
Additionally we will have smart tagging so we will need a table for that as well.

Workflows:

Save workflow
User saves some text -> mims classifies it with tags and a topic sentence. -> User is notified about success or failure.

Search workflow
User asks mims to search history for a topic -> db is searched for related interactions (tags and topic) -> results are combined and summarized then returned to the user

## An Alternative Design

the idea of having a single binary with dimple capabilities is intriguing. However, the more I play with and learn about slims etc. the more i think i want to build mims as a system with an api layer fronting microservices, that gives us the ability to decouple from the client and provide a contract for various (cli, tui, application)

In this design the shared services will be backed by a mongodb atlas cluster.

### Key Design Pricipals

- system should be extensible.
- solid api design / contract upfront.
- no special cases for individual client types.
- system should function with < 5s response times on llm respnses and < 500ms on all other functionality
	- search sevice cache
- System configurations should be stored outside of etcd to allow for easy recovery

### Services / Endpoints

#### Search
Contextual search possibly? Start with a simple tags search and then add features.

Search service should return an object with a summary of search results and common tags
plus a list of interactions.

/POST /search 

Request:
```json

{
	"term" : "",
	"context" : ""
}

```

Response:
```json
{
	"Summary" : "",
	"Tags" : ["tag1"],
	"Interactions" : [
		{
			"id" : 0,
			"tags": ["tag1","tag3"],
			"topic": "this is a topic",
			"prompt": "prompt",
			"response": "response",
			"context": "context"
		},
		{
			"id" : 1,
			"tags": ["tag1","tag2"],
			"topic": "this is a topic",
			"prompt": "prompt",
			"response": "response",
			"context": "context"
		}
	]
}

```

#### Save

Saves the common interaction object.

```python

class Interaction:
	id: int
	tags: str
	topic: str
	prompt: str
	response: str
	context: str
```

#### Ponder
- Middleware / Proxy for LLM chat requests

#### Classification

Will leverage slim models and agents from LLMware

- tagging
- topic
- sentiment

#### Summarization

- used to combine multiple search results
