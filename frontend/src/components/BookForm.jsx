function BookForm({
  formData,
  setFormData,
  editingId,
  onSubmit,
  onCancel,
  loading,
  compact = false,
}) {
  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const form = (
    <form className="form-grid" onSubmit={onSubmit}>
      <label>
        <span>Title</span>
        <input name="title" value={formData.title} onChange={handleChange} required />
      </label>

      <label>
        <span>Author</span>
        <input name="author" value={formData.author} onChange={handleChange} required />
      </label>

      <label>
        <span>Price</span>
        <input
          name="price"
          type="number"
          min="0"
          step="1"
          value={formData.price}
          onChange={handleChange}
          required
        />
      </label>

      <label>
        <span>Quantity</span>
        <input
          name="quantity"
          type="number"
          min="0"
          step="1"
          value={formData.quantity}
          onChange={handleChange}
          required
        />
      </label>

      <label>
        <span>Published date</span>
        <input name="published_date" type="date" value={formData.published_date} onChange={handleChange} />
      </label>

      <div className="form-actions">
        <button type="submit" disabled={loading}>
          {loading ? 'Đang lưu...' : editingId ? 'Lưu thay đổi' : 'Thêm sách'}
        </button>

        {editingId ? (
          <button type="button" className="secondary" onClick={onCancel} disabled={loading}>
            Hủy
          </button>
        ) : null}
      </div>
    </form>
  );

  if (compact) {
    return form;
  }

  return (
    <section className="panel book-form-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Book form</p>
          <h2>{editingId ? 'Cập nhật sách' : 'Thêm sách mới'}</h2>
        </div>
      </div>

      {form}
    </section>
  );
}

export default BookForm;
