<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="div/lg">
<p>
<xsl:copy-of select="./@*"/>
<xsl:attribute name="metrical">
<xsl:text>y</xsl:text>
</xsl:attribute>
<xsl:value-of select="."/>
</p>
</xsl:template>

</xsl:stylesheet>