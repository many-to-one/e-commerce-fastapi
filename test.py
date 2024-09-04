import base64
import hashlib


# Przykładowa faktura XML
invoice_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns="http://crd.gov.pl/wzor/2021/11/29/11089/">
    <Header>
        <InvoiceNumber>FV/2024/09/001</InvoiceNumber>
        <InvoiceDate>2024-09-04</InvoiceDate>
        <Seller>
            <Name>Firma XYZ</Name>
            <TaxID>1234567890</TaxID>
            <Address>
                <Street>Ulica Przykładowa 1</Street>
                <City>Warszawa</City>
                <PostalCode>00-001</PostalCode>
                <Country>PL</Country>
            </Address>
        </Seller>
        <Buyer>
            <Name>Firma ABC</Name>
            <TaxID>0987654321</TaxID>
            <Address>
                <Street>Ulica Testowa 2</Street>
                <City>Kraków</City>
                <PostalCode>30-002</PostalCode>
                <Country>PL</Country>
            </Address>
        </Buyer>
    </Header>
    <Items>
        <Item>
            <Description>Usługa konsultingowa</Description>
            <Quantity>1</Quantity>
            <UnitPrice>1.00</UnitPrice>
            <TotalPrice>1.00</TotalPrice>
            <VATRate>23</VATRate>
            <VATAmount>0.23</VATAmount>
        </Item>
    </Items>
    <Summary>
        <TotalNetAmount>1.00</TotalNetAmount>
        <TotalVATAmount>0.23</TotalVATAmount>
        <TotalGrossAmount>1.23</TotalGrossAmount>
    </Summary>
</Invoice>'''

# Konwersja faktury do Base64
invoice_base64 = base64.b64encode(invoice_xml.encode('utf-8')).decode('utf-8')

# Generowanie hash faktury
invoice_hash = hashlib.sha256(invoice_xml.encode('utf-8')).hexdigest()

# Obliczanie rozmiaru faktury
invoice_size = len(invoice_xml)

# Przygotowanie body żądania
body = {
    "sessionId": "twoj_session_id",
    "plain": {
        "invoice": invoice_base64
    },
    "encrypted": {
        "invoiceSize": invoice_size,
        "invoiceHash": invoice_hash,
        "encryptedInvoice": "zaszyfrowana_faktura"  # Jeśli faktura jest zaszyfrowana
    }
}

# print('*** BODY ***', body)

# Wysłanie żądania POST
response = requests.post("https://ksef-test.mf.gov.pl/api/ksef/invoice/send", json=body)

# Sprawdzenie odpowiedzi
print(response.status_code)
print(response.json())