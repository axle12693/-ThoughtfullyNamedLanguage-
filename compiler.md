
# Intro

A typical compiler does the following steps:

 - Parsing: the source text is converted to an abstract syntax tree (AST).
 - Resolution of references to other modules (C postpones this step till linking).
 - Semantic validation: weeding out syntactically correct statements that make no sense, e.g. unreachable code or duplicate declarations.
 - Equivalent transformations and high-level optimization: the AST is transformed to represent a more efficient computation with the same semantics. This includes e.g. early calculation of common subexpressions and constant expressions, eliminating excessive local assignments (see also SSA), etc.
 - Code generation: the AST is transformed into linear low-level code, with jumps, register allocation and the like. Some function calls can be inlined at this stage, some loops unrolled, etc.
 - Peephole optimization: the low-level code is scanned for simple local inefficiencies which are eliminated.

Most modern compilers (for instance, gcc and clang) repeat the last two steps once more. They use an intermediate low-level but platform-independent language for initial code generation. Then that language is converted into platform-specific code (x86, ARM, etc) doing roughly the same thing in a platform-optimized way. This includes e.g. the use of vector instructions when possible, instruction reordering to increase branch prediction efficiency, and so on.

After that, object code is ready for linking. Most native-code compilers know how to call a linker to produce an executable, but it's not a compilation step per se. In languages like Java and C# linking may be totally dynamic, done by the VM at load time.


# Remember the basics

 - Make it work
 - Make it beautiful
 - Make it efficient

This classic sequence applies to all software development, but bears repetition.

Concentrate on the first step of the sequence. Create the simplest thing that could possibly work.


# Read the books!

Read the "Dragon Book" by Aho and Ullman. This is classic and is still quite applicable today.

"Modern Compiler Design" is also praised.

If this stuff is too hard for you right now, read some intros on parsing first; usually parsing libraries include intros and examples.

Make sure you're comfortable working with graphs, especially trees. These things is the stuff programs are made of on the logical level.


# Define your language well

Use whatever notation you want, but make sure you have a complete and consistent description of your language. This includes both syntax and semantics.

It's high time to write snippets of code in your new language as test cases for the future compiler.


# Use your favorite language

It's totally OK to write a compiler in Python or Ruby or whatever language is easy for you. Use simple algorithms you understand well. The first version does not have to be fast, or efficient, or feature-complete. It only needs to be correct enough and easy to modify.

It's also OK to write different stages of a compiler in different languages, if needed.


# Prepare to write a lot of tests

Your entire language should be covered by test cases; effectively it will be defined by them. Get well-acquainted with your preferred testing framework. Write tests from day one. Concentrate on 'positive' tests that accept correct code, as opposed to detection of incorrect code.

Run all the tests regularly. Fix broken tests before proceeding. It would be a shame to end up with an ill-defined language that cannot accept valid code.


# Create a good parser

[Parser generators are many](http://en.wikipedia.org/wiki/Comparison_of_parser_generators). Pick whatever you want. You may also write your own parser from scratch, but it only worth it if syntax of your language is dead simple.

The parser should detect and report syntax errors. Write a lot of test cases, both positive and negative; reuse the code you wrote while defining the language.

Output of your parser is an abstract syntax tree.

If your language has modules, the output of the parser may be the simplest representation of 'object code' you generate. There are plenty of simple ways to dump a tree to a file and to quickly load it back.


# Create a semantic validator

Most probably your language allows for syntactically correct constructions that may make no sense in certain contexts. An example is a duplicate declaration of the same variable or passing a parameter of a wrong type. The validator will detect such errors looking at the tree.

The validator will also resolve references to other modules written in your language, load these other modules and use in the validation process. For instance, this step will make sure that the number of parameters passed to a function from another module is correct.

Again, write and run a lot of test cases. Trivial cases are as indispensable at troubleshooting as smart and complex.


# Generate code

Use the simplest techniques you know. Often it's OK to directly translate a language construct (like an if statement) to a lightly-parametrized code template, not unlike an HTML template.

Again, ignore efficiency and concentrate on correctness.


# Target a platform-independent low-level VM

I suppose that you ignore low-level stuff unless you're keenly interested in hardware-specific details. These details are gory and complex.

Your options:

 - LLVM: allows for efficient machine code generation, usually for x86 and ARM.
 - CLR: targets .NET, multiplatform; has a good JIT.
 - JVM: targets Java world, quite multiplatform, has a good JIT.



# Ignore optimization

Optimization is hard. Almost always optimization is premature. Generate inefficient but correct code. Implement the whole language before you try to optimize the resulting code.

Of course, trivial optimizations are OK to introduce. But avoid any cunning, hairy stuff before your compiler is stable.


# So what?

If all this stuff is not too intimidating for you, please proceed! For a simple language, each of the steps may be simpler than you might think.

Seeing a 'Hello world' from a program that your compiler created might be worth the effort.


Source: https://softwareengineering.stackexchange.com/questions/165543/how-to-write-a-very-basic-compiler