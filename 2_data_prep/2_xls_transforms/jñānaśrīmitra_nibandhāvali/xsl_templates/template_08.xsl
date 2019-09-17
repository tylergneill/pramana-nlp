<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="//p[ parent::div[ parent::div[@n='12'] ] ]">

[<xsl:value-of select="@n"/>]

<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="//p[ not( parent::div[ parent::div[@n='12'] ] ) ]">

[<xsl:value-of select="@page"/><xsl:text>,</xsl:text><xsl:value-of select="@page2"/>]

<xsl:value-of select="."/>
</xsl:template>

</xsl:stylesheet>