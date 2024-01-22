CREATE TABLE IF NOT EXISTS questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    author_id UUID,
    body TEXT
);

CREATE TABLE IF NOT EXISTS answers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    author_id UUID,
    question_id UUID REFERENCES questions(id) ON DELETE CASCADE,
    score INT,
    body TEXT
);
