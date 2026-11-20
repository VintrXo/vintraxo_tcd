# @lesson category-theory-composition
title: Objects, arrows, and composition
summary: In the category of sets, an arrow is a function between sets.
---
In the category of sets, an arrow is a function between sets. Compose `g∘f` when the target of f is the source of g, applying f first. The identity fixes every element. Composition in any category is associative.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
def f(x):
    return x + 1

def g(x):
    return 2 * x

print(g(f(3)), f(g(3)))
```

```exercise
? What is g(f(4)) in the example?
___
= 10
```

```quiz
? In g∘f, which function is applied first?
* f
- g
- The identity
> The output of f becomes the input to g.
```

# @lesson category-theory-isomorphism
title: Isomorphisms and inverse arrows
summary: An isomorphism has a two-sided inverse whose two compositions give the appropriate identity arrows.
---
An isomorphism has a two-sided inverse whose two compositions give the appropriate identity arrows. In sets, a bijection is an isomorphism. A map sending two elements to one output cannot be inverted to recover both inputs.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
forward = {'a': 1, 'b': 2}
backward = {value: key for key, value in forward.items()}
print(backward[forward['b']])
print(forward[backward[1]])
```

```exercise
? If f(a)=1 and f(b)=2, what does the inverse return at 2? Enter a or b.
___
= b
```

```quiz
? What does composing an arrow and its inverse yield?
- An arbitrary new arrow
* The identity arrow
- Always a constant arrow
> The two compositions giving identities are part of the definition.
```

# @lesson category-theory-functor
title: Project: a functor preserves composition
summary: A functor maps objects and arrows while preserving identities and composition.
---
A functor maps objects and arrows while preserving identities and composition. The covariant power-set functor sends a set to its subsets and a function to its direct-image map. The direct image under `g∘f` equals the image under f followed by the image under g.

## Try it yourself

Predict the output, run the example, then change one input to test the idea.

```try python
def image(function, subset):
    return {function(value) for value in subset}

subset = {1, 2}
f = lambda x: x + 1
g = lambda x: 2 * x
separate = image(g, image(f, subset))
composed = image(lambda x: g(f(x)), subset)
print(sorted(separate), separate == composed)
```

```exercise
? How many elements are in the image of {1,2} under x ↦ 2x?
___
= 2
```

```quiz
? Which properties does a functor preserve?
- Always numerical order
- Every set size
* Identities and composition
> A functor maps an identity to an identity and a composite to the corresponding composite.
```

# @lesson category-theory-reference
title: Introduction to category theory study guide
summary: Revisit the examples and review the introductory topic.
type: Reference
---
- [[category-theory-en/category-theory-composition|Objects, arrows, and composition]]
- [[category-theory-en/category-theory-isomorphism|Isomorphisms and inverse arrows]]
- [[category-theory-en/category-theory-functor|Project: a functor preserves composition]]

Review [[advanced-math-en/advanced-math-categories|the introductory lesson]] or return to [[math-branches-en/math-branches-map|the mathematics map]].
