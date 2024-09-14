import { useState } from 'react';
const Create = () => {
    const [title, setTitle] = useState('');
    const [body, setBody] = useState('');
    const [author, setAuthor] = useState('Google');

    

    const handleSubmit = (e) => {
        e.preventDefault();
        const blog = { title, body, author };

        console.log(fetch('http://localhost:8000/blogs', {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(blog)
        }).then(response => {
            if (response.ok) {
                setTitle('');
                setBody('');
                setAuthor('Google');
            }
        }));
    }

    return ( 
        <div className="create">
            <h2>Add a New Blog</h2>
            <form onSubmit={handleSubmit}>
                <label>Blog Title:</label>
                <input
                    type="text"
                    required
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
                <label>Blog Body:</label>
                <textarea
                    required
                    value={body}
                    onChange={(e) => setBody(e.target.value)}
                ></textarea>
                <label>Blog Author:</label>
                <select 
                    value={author}
                    onChange={(e) => setAuthor(e.target.value)}
                >
                    <option value="Google">Google</option>
                    <option value="Facebook">Facebook</option>
                </select>
                <button>Add Blog</button>
            </form>
        </div>
     );
}
 
export default Create;