## Inspiration
According to APA, in 2018, 39% of researched Americans reported that they don't go to therapists because they could not afford the therapy cost, time, and daycare. Our team believes that after the pandemic and also the recent high rate of price inflation, such concern is more alert. "Follow Up" is an attempt to lower the therapy cost. We aimed at reducing expensive in-person therapy sessions with accurate remote AI-powered diagnoses, requiring less therapist input and more flexibility for the patients. For now, we are focusing on determining _depression_.

## What it does
"Follow Up" creates a platform for therapists and patients to communicate after a traditional in-person session:
###- From the patient:
They will be asked to answer a questionnaire provided by the therapists, and also upload the video URLs where they answer the questions.

###- From the therapist:
After a traditional therapy session, the therapist will jot down some relevant questions. Those questions can be some self-report questions regarding how the patient feels.
The therapist will also require their patients to upload a video answering some critical questions, which they think will best reflect the patient's mental state. We introduce _Hume_ to help us detect the emotion based on their video answer.
The 5 emotions we used to suggest that a person has depression were: _Anxiety, Guilt, Tiredness, Sadness, and Distress_.  We planned to create a model to train how much each emotion weighs in terms of reflecting depression.

## How we built it
We used _Flask, HTML, and CSS_  mainly to create the full-stack development. We set up the database using _CockroachDB_ serverless, and utilize _Hume_ to help us analyze the emotion from the uploaded video.
 
## Challenges we ran into
Honestly, just try to make everything run. The first problem we had was connecting the local machine to the _CockroachDB_, as we did not have _PostgresDB_ ready. Secondly, we could not just feed any URL to the _Hume_ model, so we tried to incorporate using Google Cloud API for that. We could not find any data regarding how much each emotion relates to depression, so the emotions' weights are untrained. Lastly, we also have some problems with the _Flask_ backend.

## Accomplishments that we're proud of
This is our first hackathon so we were quite lost in brainstorming the idea at the beginning, not to mention that one teammate disappeared unannouncedly. We are proud that we stayed until the end and did not give up.

## What we learned
I personally never searched "What is" or "How to" in 24 hours this much in my life. So, in other words, a lot.

## What's next for Follow Up
We believe this has a lot of potential. This current version only focuses on _depression_, but there are a lot more symptoms we can analyze. Also, because of the lack of training data for the weight of each emotion, we believe that more research on how much of each dominant emotion is reflected in mentally ill patients will put our idea into more multi-dimensional use.
