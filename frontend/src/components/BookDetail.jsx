import BookForm from './BookForm';

function BookDetail({
  mode,
  book,
  formData,
  setFormData,
  editingId,
  onClose,
  onSubmit,
  onEdit,
  loading,
}) {
  if (!mode) {
    return null;
  }

  const isDetailMode = mode === 'detail';
  const isEditMode = mode === 'create' || mode === 'edit';
  const title = isDetailMode ? 'Chi tiết sách' : editingId ? 'Cập nhật sách' : 'Thêm sách mới';
  const accentValue = isDetailMode && book ? book.title : editingId ? 'Chỉnh sửa nội dung hiện có' : 'Tạo một đầu sách mới';

  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
      <div
        className={`modal-card ${isEditMode ? 'modal-card--wide' : ''}`}
        role="dialog"
        aria-modal="true"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="modal-header">
          <div>
            <p className="eyebrow">{isDetailMode ? 'Book detail' : 'Book form'}</p>
            <h3>{title}</h3>
          </div>
          <div className="row-actions">
            {isDetailMode && book ? (
              <button type="button" onClick={() => onEdit(book)}>
                Sửa
              </button>
            ) : null}
            <button type="button" className="secondary" onClick={onClose}>
              Đóng
            </button>
          </div>
        </div>

        <div className="modal-body">
          {isDetailMode ? (
            <div className="book-detail-summary">
              <div className="detail-spotlight">
                <div className="detail-spotlight-title">
                  <span className="eyebrow">Book spotlight</span>
                  <strong>{book.title}</strong>
                  <span className="muted">{book.author}</span>
                </div>

                <div className="detail-spotlight-meta">
                  <span className="meta-chip meta-chip--accent">ID #{book.id}</span>
                  <span className="meta-chip">{book.quantity} cuốn</span>
                  <span className="meta-chip">{book.published_date || 'Chưa có ngày xuất bản'}</span>
                </div>

                <p className="modal-note">{accentValue}</p>
              </div>

              <dl className="detail-list">
                <div>
                  <dt>Price</dt>
                  <dd>{book.price}</dd>
                </div>
                <div>
                  <dt>Quantity</dt>
                  <dd>{book.quantity}</dd>
                </div>
                <div>
                  <dt>Title</dt>
                  <dd>{book.title}</dd>
                </div>
                <div>
                  <dt>Author</dt>
                  <dd>{book.author}</dd>
                </div>
                <div>
                  <dt>Published date</dt>
                  <dd>{book.published_date || '-'}</dd>
                </div>
                <div>
                  <dt>ID</dt>
                  <dd>{book.id}</dd>
                </div>
              </dl>
            </div>
          ) : (
            <div className="modal-form-shell">
              <BookForm
                formData={formData}
                setFormData={setFormData}
                editingId={editingId}
                onSubmit={onSubmit}
                onCancel={onClose}
                loading={loading}
                compact
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default BookDetail;
