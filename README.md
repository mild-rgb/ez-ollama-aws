**ez-ollama-aws**

Since GenerativeAI became mainstream with ChatGPT, a lot has been done to democratise it. The weights and source code of foundation models that match OpenAI's offerings are routinely released, for example, DeepSeek-R1. Ollama simplifies the running of these models to a command line interface or an API. 

However, the hardware to run the models on is quite difficult to obtain. A MacBook M1 is recommended to run Llama-7B, which was released 3 years ago and is at the bottom range of available models. As the size of the model increases, the consumer hardware needed to run it becomes almost exponentially more expensive. 

However, very few applications for LLMs require being constantly available for 24 hours and therefore cloud computing becomes viable. A lot of currently available AI hosting services appear to be essentially subletting AWS for this. My personal ballpark estimate is that DeepSeekR1 could be constantly run on AWS EC2 for about 10 USD / hour, which is easily within a hobbyist budget. 

This project aims to simplify and cheapen the process of running LLMs on AWS. 

Current Features 
- initialisation and installation of orca-mini on a c4.2xlarge instance with one terminal command
- prompt model and recieve responses from the command line
- automatically shuts down instance when program is closed [no eating ramen for a week because you forgot to shut down your instance before going on holiday] 

Future Features 
- reverse ollama API proxy - allows integration with tools that assume ollama is locally installed
- commandline choice of models 


**TODO**
- rewrite main_program to use boto to connect to aws as opposed to piping commands into the terminal 
- implement support for chat history 
