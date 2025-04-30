# Preface

> This is a work in progress.
> A lot of the material is rough and in early form, especially the prose.
> However, the book development tooling is in place, so all the examples are tested (If something doesn't work, I'll
> know about it).
> My hope is that even during development you will find the material useful.

At the beginning of the book _Alice in Wonderland_, Alice sees a white rabbit wearing clothing and holding a watch.
The rabbit runs off, very concerned about being late for something, and Alice follows him.
She falls down a rabbit hole, and this leads to many bizarre and complicated adventures.
The story ends when she wakes up and realizes it was all a dream.

This is the origin of the phrase "going down a rabbit hole."
I feel silly explaining it, but I've begun having getting-old experiences where I realize that something that was
common earlier in my life has become so obsolete that all we are left with is obscure references--which I understand but
younger people don't.

A young friend rescued a typewriter from a dumpster, fascinated with all the physical mechanisms for stamping letters
onto paper.
But they were completely baffled by the way that paper got moved forward so you could start typing the next line.
I had to demonstrate the way you pushed the arm attached to the paper carriage, so that it would not only advance the
roller--that is, perform a "line feed"--but also move the carriage back to the starting position--a "carriage return."
I've seen the expressions in younger programmers when they realize that those words came from physical typewriters and
that we still carry the terms in programming today despite there being no physical analogue anymore.

At the beginning of my career, a huge portion of the programming world went down a rabbit hole called _Object-Oriented Programming_ (OOP).
That particular Wonderlandian dream has lasted for decades, but in recent years we've finally started waking up from it.
I've had a number of conversations with fellow OOP teachers, and all of us are beginning to feel quite foolish that we didn't see the illusions earlier.
But those illusions were both complex and compelling.

This book is one attempt to help undo the damage produced by the illusion of OOP.

## What's Wrong with Objects?

My first experience with OO programming was during the infancy of C++ in the mid-1980s.
I was working in the School of Oceanography at the University of Washington under Tom Keffer, who had gotten a research grant to explore making programming easier.
Our target audience was scientists and engineers, who were still primarily using Fortran, an acronym for FORmula TRANslation.
Translating formulas into Fortran was an onerous process, and we hoped to create a system where the resulting code looked like the original math equations.
The ability to create objects and to combine them with operators seemed very promising, so we settled on C++, even though it was in its infancy.

The C++ compiler had to be physically mailed to us from Bell Labs; it might even have been Bjarne Stroustrup or Andrew Koenig who did the mailing.
It arrived on a big tape reel, containing a C program that we had to compile with our local C compiler.
The standardization of the C language was years away, and every machine had their own variant of C,
so the C++ compiler had to be written in a common subset that would work with most C compilers.

Compiling this program produced `cfront` which takes your C++ code and translates it into C code.
You passed this generated C to your local C compiler to produce the resulting executable.
This approach was brilliant because it worked atop the diaspora of C compilers available at that time.

The language itself was brilliant because it was an evolution of the dominant C language.
These days we are comfortable learning new and different languages, but back then people were still getting comfortable with C (many had been assembly programmers
so the idea of a compiler was still strange), and they had very little interest in taking a chance on something that didn't feel like C.

As I burrowed my way into this new language I came across a mystery: the keyword `virtual`.
Because `cfront` emitted C code, I was able to sleuth my way through the convoluted process of dynamic binding in a statically-compiled language.
Although this seemed like a weird thing to do, I reasoned that this very weirdness meant it must be especially important.
And I, along with everyone else, began trying to understand what we were supposed to do with this new feature.

This lead to writing books, teaching, and consulting about OOP.
An industry grew up around it, and the reign of OOP influenced numerous new languages--you had to have it.

And teaching it was tough, because you had to come up with introductory examples that made some kind of sense.
Shapes and pets and colors were repeated again and again.
If a class just solved a problem but had no possibilities for inheritance, it didn't make the case for OOP so we didn't use it.

I still remember Bjarne Stroustrup saying "user-defined types" and how powerful that sounded.
He also made the distinction between _object-based_ and _object-oriented_.
The former turned out to be the very problem we wanted to solve, to liberate ourselves from the limitations of the language's built-in types.
The latter turned out to be a huge distraction.

The book _Design Patterns: Elements of Reusable Object-Oriented Software_ appeared in 1994 and answered the question, "what are we supposed to do with OOP."
It was such a success that its four primary authors garnered the nickname _Gang of Four_, and "GoF" became the shorthand way to refer to the book.
There were indeed many interesting ways to apply OOP to design problems.
The question felt answered and yet upon closer inspection, the design examples given in the book turned out to be rather obscure.
And the most confounding thing was in the preface [check this] of the book, where they said "Prefer composition to inheritance."
After writing this complicated tome about OOP, they tried to convince us, right at the beginning, to avoid it.

No one noticed the admonishment for many years, because that was not the answer we were looking for.
Asking "how do I do this?" and being answered "don't" is one of the more common jokes, and frustrating things, about programmers.
So we forged ahead and dutifully struggled to understand the GoF patterns and attempted to understand how they would be used in everyday software designs.

## Strong Typing vs. Strong Testing

## Tight vs. Permissive Type Systems

## Why is This Book Free?

When I began writing about programming, there were user manuals, but these weren't very good.
Magazine articles and books were the primary way people found information.
The demand was high, so it was relatively easy to become a book author.
I'm sure I could have made a lot more money in computing in some other way, but:

1. I enjoyed the process of discovery and of writing about it.
2. I had convinced myself that this was a good path to becoming a consultant.

Many years later, I've come to ponder point two and realized that I had jumped to a convenient conclusion based on point
one.
If I was starting out now to pursue consulting, I would instead ask a lot of questions, probably starting with an AI.
I would then talk to individual consultants and small consulting firms, and maybe even work for one.
Most importantly, I would try to get to the bottom of _why_ I wanted to be a consultant; what need does it satisfy (
other than making a living).

In my case the "why" is the need for connection and community and the need to be helpful.
In the last 15 years I've studied this thing called _Nonviolent Communication_ (NVC) and taken a lot of enjoyable
workshops on the subject.
After becoming better at communicating, the biggest benefit of NVC is discovering your true needs.
Once you know those, you can distinguish between needs and strategies--a strategy is one way to meet a need.
We humans tend to get attached to strategies and often assume that the strategy _is_ the need.
However, if you can discover and focus on your needs, it opens possibilities.
Paying attention to needs allows you to look at multiple strategies instead of getting stuck on the first one that pops
into your head.
You can evaluate strategies to see which ones are more or less possible, and which ones might meet your needs better.

I've had some very enjoyable consulting experiences,
but I wonder what things might have been like if I had seen and understood the difference between needs and strategies
sooner.

If you _do_ want to contribute financially to the book, there are ways:

1. Although the lowest price on Leanpub is `0$` and you are encouraged to use that, it's also possible to raise that
   number.
2. [Other ways? Contribute to the nonprofit? TBD]

### Creating This Book "In The Open"

A very significant benefit of giving the book away is that I can build it "in the open."
That is, I can publish it on the web as I'm creating it.
This produces:

1. Feedback. My most successful books, _Thinking in C++_ and _Thinking in Java_, were both tested on audiences many
   times before they were published in print.
   Getting feedback as early as possible, and as the book evolved, was essential in making them what they were.
2. Promotion. People are happy to tell other people about something they like that is free. There's no way to corrupt
   recommendations if there's no cost.
3. Availability. Giving away _Thinking in Java_ in the late 90's meant that anyone in the world who had an internet
   connection could get it,
   especially countries where books were expensive or prohibited in some way. And this produced more feedback.


- A "Business Model" can be about more than just money
- My goal is to create experiences. I'm not sure what form they might take, but perhaps it will be helping teams design
  types and architect their software.

## Yes, I Used AI

This is the first book I've written with AI, and it's been massively helpful.
I've used it every way that I can.
It has dramatically sped up the development of the book and my understanding of the material.

AI has been a tremendously useful assistant, far better than what we've had in the past, but:

1. I've still had to come up with the questions.
2. I've had to check, correct, and rewrite _everything_ it's produced.

To create this book, I've been as lazy as I've known how.
But as with any book, I've developed a deep understanding of the topic by writing it.
And if I've "cheated" by using AI, well, you can use the book for free, so it doesn't bother me.

The Jevons Paradox, named after the English economist William Stanley Jevons, who identified it in 1865.
Jevons observed that as coal use became more efficient, particularly with the invention of the Watt steam engine.
Coal consumption increased rather than decreased.
Increased efficiency in using a resource tends to increase (rather than decrease) the total consumption of that
resource.
Rebound effects: expected gains from efficiency are offset by behavioral or economic responses.
As AI makes programmers more efficient in creating systems, the demand for programmers will increase.

I used to have a bookcase full of computer programming books.
Then it became much easier to search the internet for answers than look in books.
Eventually I got rid of most of my books.
It's now become much easier to ask questions of an AI and have it generate examples and prose (although both must be
rewritten).
So I will tend to use AI more than other resources, still verifying as I did with those other resources.
Using the AI has taught me to be better at asking questions, and I hope this book might do the same for you.

I've enjoyed writing books, but perhaps because of AI, this will be my last one.
Perhaps I will hand over the teaching of programming to AI.
If that happens, it means that I will have moved on to building tools for programmers and building systems for
non-programmers.
Ultimately, that will be more useful than writing books about programming.
I look forward to it.

## Acknowledgements

Most of the understanding I needed to explain this topic came from my attempts to help on the
book [Effect-Oriented Programming](https://effectorientedprogramming.com/) with Bill Frasure and James Ward, that we
worked on for over four years.
I’ve also learned a lot from some of the interviews that James and I have done for
the [Happy Path Programming podcast](https://happypathprogramming.com/).
