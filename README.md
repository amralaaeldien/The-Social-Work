# Helper - مساعد
A simple social network devoted to promoting and helping charitable work and charity organizations thrive by giving them functionalities that should help them achieve their goals easier and more efficiently. Helper has much more functionality than what is presented here, what is presented here are the features that I have develped myself from mere ideas to development.

# Technologies
* Python
* Django

# Features 
The portion of Helper that is presented here is a paltform that helps needers(people who need help) get connected to helpers(people who offer help) by providing a platform that optimizes this connection by its features. Please note that not all the features are implemented.
* The needers could be individuals or organizations, helpers could also be individuals or organizations, so there are two types of users on this platform which are : idividuals and organizations.
* There are two types of posts which are : needers' posts and helpers' posts.
* There is a voting system with an upvote and only upvote - no down vote - on posts and comments, the reason why there is only an upvote and no downvote is that all kinds of problems that needers might need help with are welcome on Helper, so there are only two possibilities, either the post represents an actual problem that the user is facing(which are welcome on Helper), or not, in the latter case we have the feature of reporting the post to the admins.
* The poster of the post has the ability to mark their post as fulfilled, which means that the need of the needer has been met in the case of a needer's post or that the ability to offer the help is no longer available in the case of a helper post. either case the post then is removed from the stack of posts. Although the fulfilled posts can be accessed separately
* The needer's posts are further subdivided into urgent and non-urgennt. the "urgent" status of the post is determined by the writer of the post at the time of creation of the post, "urgent" means that the needer needs his problem to be resolved in the next few hours. Why wouldn't the users abuse the "urgent" status? I rely on the assumption that the urgent and non-urgent sections would balance each other, meaning if everyone tried to mark their post as urgent, the section of "non-urgent posts" would be relatively empty and would make a better means for your post to be observed by helpers, and vice versa.
