import 'jsr:@supabase/functions-js/edge-runtime.d.ts'

const session = new Supabase.ai.Session('gte-small');

Deno.serve(async (req) => {
  try {
    // Extract text for summarization
    const { description } = await req.json();

    if (!description || typeof description !== 'string') {
      return new Response(
        JSON.stringify({ error: 'Description is missing or invalid.' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const input = "Summarise the following text: " + description;

    // Generate short summary
    const summary = await session.run(input, {
      normalize: true,
      mean_pool: true
    });

    // Return summary
    return new Response(
      JSON.stringify({ summary }),
      { headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    console.error('Error processing request:', error);
    return new Response(
      JSON.stringify({ error: 'Internal server error.' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
});
