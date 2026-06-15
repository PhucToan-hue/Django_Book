function formatCurrency(value) {
  return new Intl.NumberFormat('vi-VN').format(value);
}

function BookTable({ books, onDetail, onEdit, onDelete }) {
  if (books.length === 0) {
    return <div className="empty-state">Không có sách phù hợp.</div>;
  }

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Author</th>
            <th>Price</th>
            <th>Quantity</th>
            <th>Published date</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {books.map((book) => (
            <tr key={book.id}>
              <td>{book.id}</td>
              <td>{book.title}</td>
              <td>{book.author}</td>
              <td>{formatCurrency(book.price)} VNĐ</td>
              <td>{book.quantity}</td>
              <td>{book.published_date || '-'}</td>
              <td>
                <div className="row-actions">
                  <button type="button" className="secondary" onClick={() => onDetail(book.id)}>
                    Detail
                  </button>
                  <button type="button" className="secondary" onClick={() => onEdit(book)}>
                    Edit
                  </button>
                  <button type="button" className="danger" onClick={() => onDelete(book)}>
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default BookTable;
