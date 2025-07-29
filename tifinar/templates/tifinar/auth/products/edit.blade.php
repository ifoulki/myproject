
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>✏️ تعديل المنتج</title>

    <!-- Bootstrap RTL -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600&display=swap" rel="stylesheet">

    <style>
        body {
            background-color: #f9fafb;
            font-family: 'Cairo', sans-serif;
        }

        .container {
            max-width: 800px;
            background-color: white;
            padding: 30px;
            margin-top: 60px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }

        h2 {
            color: #0d6efd;
            margin-bottom: 25px;
        }

        label {
            font-weight: 600;
            color: #333;
        }

        .form-control {
            border-radius: 10px;
        }

        .form-control:focus {
            border-color: #0d6efd;
            box-shadow: 0 0 0 0.15rem rgba(13,110,253,.15);
        }

        .btn-primary {
            padding: 10px 25px;
            border-radius: 10px;
            font-weight: bold;
        }

        .btn-primary i {
            margin-left: 8px;
        }

        .image-preview img {
            border-radius: 10px;
            border: 1px solid #ddd;
            margin: 5px;
            transition: transform 0.3s;
        }

        .image-preview img:hover {
            transform: scale(1.05);
        }
    </style>
</head>
<body>

<div class="container">
    <h2><i class="fas fa-pen"></i> تعديل منتج</h2>

    @if(session('success'))
        <div class="alert alert-success">{{ session('success') }}</div>
    @endif

    <form action="{{ route('auth.products.update', $product->id) }}" method="POST" enctype="multipart/form-data">
        @csrf
        @method('PUT')

        <div class="mb-3">
            <label for="images">صور جديدة (اختياري)</label>
            <input type="file" name="images[]" class="form-control" multiple accept="image/*">
        </div>

        @if($product->image_filenames)
            <div class="mb-3">
                <label>الصور الحالية:</label>
                <div class="d-flex flex-wrap image-preview">
                    @foreach(explode(',', $product->image_filenames) as $img)
                        <img src="{{ asset('images/products/' . $img) }}" width="100" height="100" alt="صورة المنتج">
                    @endforeach
                </div>
            </div>
        @endif

        <div class="mb-3">
            <label for="name_in_arabic">الاسم بالعربية</label>
            <input type="text" name="name_in_arabic" class="form-control" value="{{ old('name_in_arabic', $product->name_in_arabic) }}" required>
        </div>

        <div class="mb-3">
            <label for="name_in_french">الاسم بالفرنسية</label>
            <input type="text" name="name_in_french" class="form-control" value="{{ old('name_in_french', $product->name_in_french) }}">
        </div>

        <div class="mb-3">
            <label for="name">الاسم العام</label>
            <input type="text" name="name" class="form-control" value="{{ old('name', $product->name) }}">
        </div>

        <hr>

        <div class="mb-3">
            <label for="description">الوصف الإنجليزية</label>
            <textarea dir="ltr" name="description" class="form-control" rows="3">{{ old('description', $product->description) }}</textarea>
        </div>
        <div class="mb-3">
            <label for="arabic_description">الوصف بالعربية</label>
            <textarea name="arabic_description" class="form-control" rows="3">{{ old('arabic_description', $product->arabic_description) }}</textarea>
        </div>
        <div class="mb-3">
            <label for="french_description">الوصف بالفرنسية</label>
            <textarea dir="ltr" name="description" class="form-control" rows="3">{{ old('french_description', $product->french_description) }}</textarea>
        </div>

        <hr>

        <div class="mb-3">
            <label for="category">الفئة</label>
            <input type="text" name="category" class="form-control" value="{{ old('category', $product->category) }}">
        </div>

        <div class="mb-3">
            <label for="purchase_price">سعر الشراء</label>
            <input type="number" name="purchase_price" class="form-control" step="0.01" min="0" value="{{ old('purchase_price', $product->purchase_price) }}">
        </div>

        <div class="mb-3">
            <label for="selling_price">سعر البيع</label>
            <input type="number" name="selling_price" class="form-control" step="0.01" min="0" value="{{ old('selling_price', $product->selling_price) }}">
        </div>

        <button type="submit" class="btn btn-primary">
            <i class="fas fa-save"></i> تحديث المنتج
        </button>
    </form>
</div>

<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>