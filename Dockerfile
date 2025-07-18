# -------- Stage 1: Builder --------
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies in a virtualenv path to reduce layer size
RUN python -m venv /venv && \
    /venv/bin/pip install --no-cache-dir --upgrade pip && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy entire source code
COPY . .

# -------- Stage 2: Runner --------
FROM python:3.11-slim AS runner

WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /venv /venv
COPY --from=builder /app /app

# Use venv path as default python/pip/uvicorn
ENV PATH="/venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
