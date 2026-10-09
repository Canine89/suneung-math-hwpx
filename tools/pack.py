"""폴더를 hwpx로 압축 (mimetype 무압축·맨 앞)."""
import os, sys, zipfile

def pack(src_dir, out_path):
    with zipfile.ZipFile(out_path, "w") as z:
        z.write(os.path.join(src_dir, "mimetype"), "mimetype", compress_type=zipfile.ZIP_STORED)
        for root, _, files in os.walk(src_dir):
            for f in sorted(files):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, src_dir).replace("\\", "/")
                if rel == "mimetype":
                    continue
                z.write(full, rel, compress_type=zipfile.ZIP_DEFLATED)

if __name__ == "__main__":
    pack(sys.argv[1], sys.argv[2])
