"""
Verify all image links in Magic Companion articles
"""
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

def verify_articles():
    """Verify all articles and their image links"""
    article_dir = "RULES/Magic-Companion"
    image_dir = "CB77028_Magic_Companion_Pages"
    
    issues = []
    verified_count = 0
    
    # Check if directories exist
    if not os.path.exists(article_dir):
        print(f"ERROR: Article directory not found: {article_dir}")
        return False
    
    if not os.path.exists(image_dir):
        print(f"ERROR: Image directory not found: {image_dir}")
        return False
    
    # Get all markdown files (excluding index)
    md_files = [f for f in os.listdir(article_dir) if f.endswith('.md') and f != 'Magic-Companion-Index.md']
    
    print(f"Verifying {len(md_files)} articles...\n")
    
    for md_file in sorted(md_files):
        filepath = os.path.join(article_dir, md_file)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all image references
        image_pattern = r'!\[Page \d+\]\((.*?)\)'
        matches = re.findall(image_pattern, content)
        
        if not matches:
            issues.append(f"{md_file}: No image references found")
            continue
        
        # Verify each image path
        all_valid = True
        for image_path in matches:
            # Convert relative path to absolute
            # Paths are like: ../../CB77028_Magic_Companion_Pages/page_XXXX.png
            if image_path.startswith('../../'):
                actual_path = image_path.replace('../../', '')
            elif image_path.startswith('../'):
                actual_path = image_path.replace('../', '')
            else:
                actual_path = image_path
            
            full_path = os.path.join(os.getcwd(), actual_path)
            
            if not os.path.exists(full_path):
                issues.append(f"{md_file}: Missing image {image_path}")
                all_valid = False
        
        if all_valid:
            verified_count += 1
            print(f"✓ {md_file}: {len(matches)} images verified")
    
    # Verify image directory has expected files
    expected_images = [f"page_{i:04d}.png" for i in range(1, 114)]
    missing_images = []
    for img_file in expected_images:
        img_path = os.path.join(image_dir, img_file)
        if not os.path.exists(img_path):
            missing_images.append(img_file)
    
    print(f"\n{'='*60}")
    print(f"Verification Summary:")
    print(f"  Articles verified: {verified_count}/{len(md_files)}")
    print(f"  Total image files: {len([f for f in os.listdir(image_dir) if f.endswith('.png')])}")
    
    if missing_images:
        print(f"  Missing images: {len(missing_images)}")
        issues.append(f"Missing {len(missing_images)} image files in {image_dir}")
    
    if issues:
        print(f"\n{'='*60}")
        print("Issues Found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"\n✓ All links verified successfully!")
        return True

if __name__ == "__main__":
    success = verify_articles()
    sys.exit(0 if success else 1)










