<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="lg">
<p>
<xsl:copy-of select="./@*"/>
<xsl:attribute name="pb">
<xsl:value-of select="preceding::pb[1]/@n"/>
</xsl:attribute>
<xsl:attribute name="ll">
<xsl:value-of select="preceding::pb[1]/@logical_locus"/>
</xsl:attribute>
<xsl:copy-of select="./node()"/>
</p>
</xsl:template>

</xsl:stylesheet>