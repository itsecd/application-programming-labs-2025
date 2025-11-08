import func
import re


def main():
    filenames = func.get_args()
    text = func.read_file(filenames[0])
    people = text.split("\n\n")
    
    emails = []
    for person in people:
        surname_match = re.search(r'Фамилия:\s*(.+)', person)
        contact_match = re.search(r'Номер телефона или email:\s*(.+)', person)
        
        if surname_match and contact_match:
            surname = surname_match.group(1).strip()
            contact = contact_match.group(1).strip()
            
            if func.is_valid_email(contact):
                emails.append(f"{surname}: {contact}")
    
    with open(filenames[1], "w", encoding="utf-8") as file:
        func.write_emails(file, emails)


if __name__ == "__main__":
    main()