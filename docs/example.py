import BootIntegrityValidator

#####################################################################################
#
# Pass in the Known Good Values file to initialize the BootIntegrityValidator
# known_good_values should be bytes.
#   This is a JSON file that has been generated by Cisco that contains the all the
#   known good values for the Boot 0, Boot Loader and OS Hash that will be used
#   to compare the output from a device
#
# known_good_values_signature should be bytes. (optional)
#   This is a signed sha-512 hash of the known_good_values file.  This is signed
#   using a Cisco Signing certificate (subject-name CN=KnownGoodValuesPROD, OU=REL, O=Cisco)
#
# custom_signing_cert should be a file-like object (optional)
#   If the certificate used to signed the known_good_values is not
#   (subject-name CN=KnownGoodValuesPROD, OU=REL, O=Cisco) (See Known_Good_Values_PROD.pem)
#   then the different signing cert can be provided.  The signing certificate MUST be
#   Signed by the Cisco CAs.  The file-like object should contain the x509 in PEM format
#
#####################################################################################

kgv = open("example_kgv.json", "rb")
biv = BootIntegrityValidator.BootIntegrityValidator(known_good_values=kgv.read())

#####################################################################################
#
# Pass in the CLI output that has been save to file:
#       show platform sudi
#    and
#       show platform integrity
#
#####################################################################################
show_plat_suid = open("example_show_plat_sudi.txt", "r")
suid = show_plat_suid.read()

show_plat_int = open("example_show_plat_int.txt", "r")
spi = show_plat_int.read()

#####################################################################################
#
# The validate function will raise specific exceptions if validation fails
# or it is unable to validate the output.
#
#####################################################################################

try:
    biv.validate(show_platform_integrity_cmd_output=spi,
                 show_platform_sudi_certificate_cmd_output=suid)
    print("Successfully validated!")

except BootIntegrityValidator.BootIntegrityValidator.InvalidFormat:
    print("know_good_values had an invalid format")

except BootIntegrityValidator.BootIntegrityValidator.VersionNotFound:
    print("Version of software Not Found in known_good_values")

except BootIntegrityValidator.BootIntegrityValidator.ProductNotFound:
    print("Product in cli output not mapped to 'product' in known_good_values")

except BootIntegrityValidator.BootIntegrityValidator.ValidationException:
    print("Validation failed")
