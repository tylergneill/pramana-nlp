<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="teiHeader|back|ref|note|anchor|lb|pb|comment()" />

<xsl:template match="q[@type='variant']" />

<xsl:template match="supplied">
<xsl:value-of select="."/>
</xsl:template>

</xsl:stylesheet>