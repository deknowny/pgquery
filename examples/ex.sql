SELECT jsonb_agg(
    jsonb_build_object(
        'full_name', author.full_name,
        'bio', author.bio,
        'books', books.books,
    )
) FROM author, LATERAL (
    SELECT jsonb_agg(
        jsonb_build_object(
            'id', boot.id,
            'title', book.title,
        )
    ) books
    FROM book
    WHERE book.author_id == author.id
) books
