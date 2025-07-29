<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>إضافة منتج</title>
    <!-- Bootstrap 5 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <!-- Font Awesome Icons -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
            padding-top: 40px;
            font-family: 'Cairo', sans-serif;
        }
        .form-container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            max-width: 600px;
            margin: auto;
        }
    </style>
</head>
<body>

    @if ($errors->any())
        <div class="alert alert-danger">
            <strong>حدثت أخطاء:</strong>
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif


<div class="container">
    <div class="form-container">
        <h3 class="mb-4 text-center"><i class="fas fa-box-open text-primary"></i> إضافة منتج جديد</h3>

        @if(session('success'))
            <div class="alert alert-success">
                <i class="fas fa-check-circle"></i> {{ session('success') }}
            </div>
        @endif

        <form action="{{ route('auth.products.store') }}" method="POST" enctype="multipart/form-data">
            @csrf

            <div class="mb-3">
                <label class="form-label">إسم المنتج <i class="fas fa-tag"></i></label>
                <input type="text" class="form-control" name="name_in_arabic" value="{{ old('name_in_arabic') }}" >
            </div>

            <div class="mb-3">
                <label for="images">تحميل صور المنتج:</label>
                <input type="file" name="images[]" id="images" multiple class="form-control">
                <div id="image-preview" class="mt-3 d-flex flex-wrap gap-2"></div>
            </div>            

            <div class="mb-3">
                <label class="form-label">إسم المنتج الفرنسية <i class="fas fa-tag"></i></label>
                <input type="text" class="form-control" name="name_in_french" value="{{ old('name_in_french') }}" >
            </div>

            <div class="mb-3">
                <label class="form-label">إسم المنتج بالإنجليزية <i class="fas fa-tag"></i></label>
                <input type="text" class="form-control" name="name" value="{{ old('name') }}" >
            </div>

            <hr>

            <div class="mb-3">
                <label class="form-label">الوصف بالإنجليزية<i class="fas fa-align-left"></i></label>
                <textarea dir="ltr" class="form-control" name="description" rows="3">{{ old('description') }}</textarea>
            </div>
            <div class="mb-3">
                <label class="form-label">الوصف بالعربية<i class="fas fa-align-left"></i></label>
                <textarea class="form-control" name="arabic_description" rows="3">{{ old('arabic_description') }}</textarea>
            </div>
            <div class="mb-3">
                <label class="form-label">الوصف الفرنسية<i class="fas fa-align-left"></i></label>
                <textarea dir="ltr" class="form-control" name="french_description" rows="3">{{ old('french_description') }}</textarea>
            </div>

            <div class="mb-3">
                <label class="form-label">التصنيف <i class="fas fa-layer-group"></i></label>
                <input type="text" class="form-control" name="category" value="{{ old('category') }}" >
            </div>

            <hr>

            <div class="mb-3">
                <label class="form-label">سعر الشراء <i class="fas fa-money-bill-wave"></i></label>
                <input type="number" class="form-control" name="purchase_price" value="{{ old('purchase_price') }}" >
            </div>

            <div class="mb-3">
                <label class="form-label">سعر البيع <i class="fas fa-coins"></i></label>
                <input type="number" class="form-control" name="selling_price" value="{{ old('selling_price') }}" >
            </div>

            <button type="submit" class="btn btn-success w-100">
                <i class="fas fa-plus-circle"></i> إضافة المنتج
            </button>
        </form>
    </div>
</div>

<!-- Bootstrap JS (اختياري للوظائف التفاعلية) -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>
    document.getElementById('images').addEventListener('change', function(event) {
        const preview = document.getElementById('image-preview');
        preview.innerHTML = '';
        Array.from(event.target.files).forEach(file => {
            const reader = new FileReader();
            reader.onload = e => {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.style.width = '100px';
                img.style.height = '100px';
                img.style.objectFit = 'cover';
                img.classList.add('rounded', 'shadow');
                preview.appendChild(img);
            };
            reader.readAsDataURL(file);
        });
    });
</script>

    
</body>
</html>

