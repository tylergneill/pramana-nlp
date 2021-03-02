Notes on data structure.

Visual demonstration:
	{...}
	[...]
	~~~
	[...]
	~~~(...)~~~
	[...]
	~~~
	{...}
	<...>
	[...]
	~~~(...)~~~<...>~~~
	[...]
	~~~

~~~ = textual content
... = element label content

Element details:

	[...] are for document identifiers (e.g. verse, paragraph).
		Every file must have these.
		In-line, these are interpreted as editorial additions, and their content is kept.

	{...} are for document group identifiers (e.g. section header).
		Only documents within sections marked off by these will be resized with each other.
		Every file must start with one of these (if only giving the title of the entire text).

	<...> are for marking additional text structure.
		These are simply discarded.

	(...) are for marking editorial/philological notes.
		These are also simply discarded in NLP preprocessing.
		This includes in-line, where these are interpreted as editorial deletions.

	Whitespace surrounding the removable elements <...> (...) is not discarded. That is, these elements must be placed so as to remove cleanly and not interfere with the spacing of textual content.

	All whitespace surrounding retained elements is discarded.